import pandas as pd
import numpy as np

def process_well_data_optimized(df_, inputs, ssp, sp_baseline, shale_phid, shale_phi_n,
                                sp_shift=0,Maximum_gr=150, Minimum_gr=15,rw=0.05, Temp_rw=78, invasion= None, rza= None, a=1, m=2, n=2):
    #The output is (phi average, phi average filtered, Temperature, Rmf corrected, Rw_corrected, Rwa, Sw, Sxo, MHI, Bvw, Delta Bvw)

    # Precompute gradients and surface temperatures for all wells
    def temp_grad(well):
      well_data = inputs.loc[inputs['Well'] == well]
      gradient = (well_data['T_max'].squeeze() - well_data['T_values'].squeeze()) * 100 / well_data['TVD'].squeeze()
      surf_temp = well_data['T_values'].squeeze()
      return gradient, surf_temp

    temp_grad_dict = {
        well: temp_grad(well) for well in inputs['Well'].unique()
    }

    def rmf_corr(well):
      well_data = inputs.loc[inputs['Well'] == well]
      rmf = well_data['Rmf'].squeeze()
      T = well_data['T_values'].squeeze()
      return rmf, T

    rmf_corr_dict = {
        well: rmf_corr(well) for well in inputs['Well'].unique()
    }

    # Precompute phi_avg to avoid recalculations
    df_['phi_avg_calc'] = np.sqrt((df_['PHIN']**2 + df_['PHID']**2) / 2)
    df_['phi_avg_calc_filtered'] = df_['phi_avg_calc'].apply(lambda x: x if x >= 0 else np.nan)

    # Compute temperature and Rmf corrected values

    df_['T'] = df_.apply(lambda row: temp_grad_dict[row['Well_Name']][0] * row['DEPTH'] / 100 +
                         temp_grad_dict[row['Well_Name']][1], axis=1)

    df_['Rmf_corrected'] = df_.apply(lambda row: rmf_corr_dict[row['Well_Name']][0] *
                           (rmf_corr_dict[row['Well_Name']][1] + 6.77) /
                           (row['T'] + 6.77), axis=1)

    # Compute temperature and Rmf corrected values
    df_['Rw_corrected'] = df_.apply(lambda row: rw *(Temp_rw + 6.77) / (row['T'] + 6.77), axis=1)

    #Apparanet water resistivity Rwa
    df_['Rwa'] = df_['Deep_Resistivity']*df_['phi_avg_calc']**m/a

    # Vectorized Sw calculation
    df_['Sw'] = (df_['Rw_corrected']*a / (df_['Deep_Resistivity'] * df_['phi_avg_calc_filtered']**m))**(1/n)

    if rza is not None:
      df_['Sxo'] = df_.apply(lambda row:
                           (a * rza /
                            (row['Shallow_Resistivity'] * row['phi_avg_calc_filtered']**m))**(1/n), axis=1)
    elif invasion is None:
      df_['Sxo'] = df_.apply(lambda row:
                           (a * row['Rmf_corrected'] /
                            (row['Shallow_Resistivity'] * row['phi_avg_calc_filtered']**m))**(1/n), axis=1)
    else:
      # Vectorized Sxo calculation
      inv_depths = {'very deep': 0.025, 'deep': 0.035, 'average': 0.05, 'shallow': 0.075, 'very shallow': 0.1}

      z = inv_depths[invasion]  # Default invasion depth
      df_['Sxo'] = df_.apply(lambda row:
                           (a * (1 / ((z / row['Rw_corrected']) + ((1 - z) / row['Rmf_corrected']))) /
                            (row['Shallow_Resistivity'] * row['phi_avg_calc_filtered']**m))**(1/n), axis=1)

    # MHI and BVW
    df_['MHI'] = df_['Sw'] / df_['Sxo']
    df_['Bvw'] = df_['phi_avg_calc_filtered'] * df_['Sw']
    df_['delta_Bvw'] = df_['Bvw'].diff().fillna(0)
    df_=calculate_shale_volume(df_,Maximum_gr=Maximum_gr,Minimum_gr=Minimum_gr,
                              ssp=ssp,sp_baseline=sp_baseline,sp_shift=sp_shift,
                               shale_phid=shale_phid,shale_phi_n=shale_phi_n)
    return df_

def calculate_shale_volume(df, Maximum_gr, Minimum_gr, ssp, sp_baseline, sp_shift, shale_phid, shale_phi_n):
    """
    Calculate shale volume (Vsh) using three different techniques and append the results to the full DataFrame.

    Parameters:
    - df (pd.DataFrame): Well log DataFrame
    - Maximum_gr (float): Maximum gamma ray deflection
    - Minimum_gr (float): Minimum gamma ray deflection
    - ssp (float): Static Spontaneous Potential
    - sp_baseline (float): SP baseline value
    - sp_shift (float): SP shift value
    - shale_phid (float): Shale density porosity
    - shale_phi_n (float): Shale neutron porosity

    Returns:
    - pd.DataFrame: Updated DataFrame with new Vsh columns appended.
    """

    # First Technique: Gamma Ray Deflection Vsh
    df['Vsh_gamma_ray'] = (df['GR'] - Minimum_gr) / (Maximum_gr - Minimum_gr)

    # Second Technique: SP-Based Vsh
    sp_shifted = df['SP'] + sp_shift
    df['Vsh_sp'] = 1 - (sp_shifted - sp_baseline) / ssp

    # Third Technique: Porosity-Based Vsh
    df['Vsh_porosity'] = (df['PHIN'] - df['PHID']) / (shale_phi_n - shale_phid)

    # Return the full DataFrame with new columns
    return df