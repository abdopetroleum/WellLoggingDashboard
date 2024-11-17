import matplotlib.pyplot as plt
import numpy as np


class WellLogPlotter:
    def __init__(self, df, sp_shift=0):
        self.df = df
        self.sp_shift = sp_shift  # New variable to shift SP log
        self.MIN_DEPTH = df['DEPTH'].min()
        self.MAX_DEPTH = df['DEPTH'].max()
        self.TEXT_SPACING_ABOVE_AXIS = 0.02
        self.AXIS_SPACING = 0.04
        self.FIGSIZE = (30, 18)
        self.fig = plt.figure(figsize=self.FIGSIZE)
        self.gamma_ray_and_main_ax = None

    def configure_axis(self, axis, label, color, x_ticks, tick_labels, linestyle='-', label_coord_offset=0.02,
                       tick_fontsize=14, y_tick_fontsize=20):  # Increased fontsize for better visibility
        axis.set_xlabel(label, fontsize=14, weight='bold', color=color)
        axis.xaxis.set_label_position('top')
        axis.xaxis.set_label_coords(0.5, 1 + label_coord_offset)
        axis.tick_params(axis='x', colors=color, labeltop=True, labelbottom=False,
                         labelsize=tick_fontsize)  # Set tick label size
        axis.tick_params(axis='y', labelsize=y_tick_fontsize)  # Y-axis tick label size
        axis.spines['top'].set_color(color)
        axis.spines['top'].set_linestyle(linestyle)
        axis.set_xticks(x_ticks)
        axis.set_xticklabels(tick_labels, fontsize=tick_fontsize, color=color)


    def plot_main_log(self):
        self.gamma_ray_and_main_ax = self.fig.add_axes([0, 0.05, 0.2, 0.9])
        bit_size_ax = self.gamma_ray_and_main_ax.twiny()
        caliper_ax = self.gamma_ray_and_main_ax.twiny()
        sp_ax = self.gamma_ray_and_main_ax.twiny()  # New SP log axis
        rwa_ax = self.gamma_ray_and_main_ax.twiny()  # New Rwa log axis

        # Plot Gamma Ray
        self.gamma_ray_and_main_ax.plot(self.df['GR'], self.df['DEPTH'], 'g-')
        self.gamma_ray_and_main_ax.set_xlim(0, 150)
        self.gamma_ray_and_main_ax.set_ylim(self.MIN_DEPTH, self.MAX_DEPTH)
        self.gamma_ray_and_main_ax.invert_yaxis()
        self.configure_axis(self.gamma_ray_and_main_ax, "GAMMA RAY", 'green', np.arange(0, 151, 15),
                            [str(int(tick)) for tick in np.arange(0, 151, 15)])
        # Set y-axis ticks and minor ticks
        self.gamma_ray_and_main_ax.set_yticks(np.arange(self.MIN_DEPTH, self.MAX_DEPTH + 10, 10))
        self.gamma_ray_and_main_ax.set_yticks(np.arange(self.MIN_DEPTH, self.MAX_DEPTH + 2, 2), minor=True)

        self.gamma_ray_and_main_ax.tick_params(axis='y', which='minor', length=4, color='gray',
                                               labelsize=12)  # Minor tick settings
        self.gamma_ray_and_main_ax.grid(True, which='major', linestyle='-', linewidth=2, alpha=0.9)
        self.gamma_ray_and_main_ax.grid(True, which='minor', linestyle='--', linewidth=0.9, alpha=0.7)

        # Plot Bit Size
        bit_size_ax.plot(self.df['BIT'], self.df['DEPTH'], 'orange')
        bit_size_ax.set_xlim(6, 16)
        bit_size_ax.spines["top"].set_position(("axes", 1 + self.AXIS_SPACING))
        self.configure_axis(bit_size_ax, "BIT SIZE", 'orange', np.arange(6, 17, 1), [str(i) for i in range(6, 17)],
                            label_coord_offset=self.AXIS_SPACING + self.TEXT_SPACING_ABOVE_AXIS)
        bit_size_ax.grid(False)

        # Plot Caliper
        caliper_ax.plot(self.df['CALI'], self.df['DEPTH'], 'b--')
        caliper_ax.set_xlim(6, 16)
        caliper_ax.spines["top"].set_position(("axes", 1 + 2 * self.AXIS_SPACING))
        self.configure_axis(caliper_ax, "CALIPER", 'blue', np.arange(6, 17, 1), [str(i) for i in range(6, 17)],
                            linestyle=(0, (5, 5)),
                            label_coord_offset=2 * self.AXIS_SPACING + self.TEXT_SPACING_ABOVE_AXIS)
        caliper_ax.grid(False)

        # Plot SP Log with Shift
        sp_ax.plot(self.df['SP'] + self.sp_shift, self.df['DEPTH'], 'purple')
        sp_ax.set_xlim(self.df['SP'].min(), self.df['SP'].min() + 20 * 10)
        sp_ax.spines["top"].set_position(("axes", 1 + 3 * self.AXIS_SPACING))

        sp_xticks = np.arange(self.df['SP'].min(), self.df['SP'].min() + 20 * 10 + 1, 20)
        sp_ax.tick_params(axis='x', which='both', top=True, labeltop=True)
        self.configure_axis(sp_ax, "SP LOG (20 mV)", 'purple', sp_xticks, [str(int(tick)) for tick in sp_xticks],
                            label_coord_offset=3 * self.AXIS_SPACING + self.TEXT_SPACING_ABOVE_AXIS)
        sp_ax.grid(False)

        # Plot Rwa
        rwa_ax.plot(self.df['Rwa'], self.df['DEPTH'], 'black')
        rwa_ax.set_xlim(0, 0.5)
        rwa_ax.spines["top"].set_position(("axes", 1 + 4 * self.AXIS_SPACING))
        self.configure_axis(rwa_ax, "Rwa", 'black', np.arange(0, 0.55, 0.05),
                            [f"{tick:.2f}" for tick in np.arange(0, 0.55, 0.05)],
                            label_coord_offset=4 * self.AXIS_SPACING + self.TEXT_SPACING_ABOVE_AXIS)
        rwa_ax.grid(False)

        # Shade area between Bit Size and Caliper where Bit Size > Caliper (Mud Cake)
        mask_mud_cake = self.df['BIT'] > self.df['CALI']
        bit_size_ax.fill_betweenx(
            self.df['DEPTH'], self.df['BIT'], self.df['CALI'],
            where=mask_mud_cake, facecolor='brown', alpha=0.3, label='Mud Cake'
        )

    def plot_resistivity_logs(self):
        deep_resistivity_ax = self.fig.add_axes([0.25, 0.05, 0.2, 0.9], sharey=self.gamma_ray_and_main_ax)
        medium_resistivity_ax = deep_resistivity_ax.twiny()
        shallow_resistivity_ax = deep_resistivity_ax.twiny()

        log_ticks = [0.2, 1, 10, 100, 2000]

        # Plot Deep Resistivity
        deep_resistivity_ax.plot(self.df['Deep_Resistivity'], self.df['DEPTH'], 'r-')
        deep_resistivity_ax.set_xscale('log')
        deep_resistivity_ax.set_xlim(0.2, 2000)
        self.configure_axis(deep_resistivity_ax, "DEEP RESISTIVITY", 'red', log_ticks,
                            [str(tick) for tick in log_ticks])
        deep_resistivity_ax.grid(True, which='major', linestyle='-', linewidth=2, alpha=0.9)  # Solid major grid
        deep_resistivity_ax.grid(True, which='minor', linestyle='--', linewidth=0.9, alpha=0.7)  # Dashed minor grid

        # Plot Medium Resistivity
        medium_resistivity_ax.plot(self.df['Medium_Resistivity'], self.df['DEPTH'], 'purple')
        medium_resistivity_ax.set_xscale('log')
        medium_resistivity_ax.set_xlim(0.2, 2000)
        medium_resistivity_ax.spines["top"].set_position(("axes", 1 + self.AXIS_SPACING))
        self.configure_axis(medium_resistivity_ax, "MEDIUM RESISTIVITY", 'purple', log_ticks,
                            [str(tick) for tick in log_ticks],
                            label_coord_offset=self.AXIS_SPACING + self.TEXT_SPACING_ABOVE_AXIS)
        medium_resistivity_ax.grid(False)

        # Plot Shallow Resistivity
        shallow_resistivity_ax.plot(self.df['Shallow_Resistivity'], self.df['DEPTH'], 'brown')
        shallow_resistivity_ax.set_xscale('log')
        shallow_resistivity_ax.set_xlim(0.2, 2000)
        shallow_resistivity_ax.spines["top"].set_position(("axes", 1 + 2 * self.AXIS_SPACING))
        self.configure_axis(shallow_resistivity_ax, "SHALLOW RESISTIVITY", 'brown', log_ticks,
                            [str(tick) for tick in log_ticks],
                            label_coord_offset=2 * self.AXIS_SPACING + self.TEXT_SPACING_ABOVE_AXIS)
        shallow_resistivity_ax.grid(False)

    def plot_porosity_logs(self):
        phid_ax = self.fig.add_axes([0.5, 0.05, 0.2, 0.9], sharey=self.gamma_ray_and_main_ax)  # Density Porosity first
        phin_ax = phid_ax.twiny()  # Neutron Porosity second (on top)
        phi_avg_ax = phid_ax.twiny()  # Average Porosity axis (new)
        rnml_ax = phid_ax.twiny()  # RNML axis (first resistivity)
        rlml_ax = phid_ax.twiny()  # RLML axis (second resistivity)
        density_corr_ax = phid_ax.twiny()
        # Set new limits for all porosity plots
        x_min, x_max = -0.15, 0.45  # Corresponds to -15% and 45%

        # Generate exact major and minor ticks
        major_ticks = np.linspace(x_min, x_max, 5)  # Major ticks at -0.15, 0.0, 0.15, 0.30, 0.45
        minor_ticks = np.arange(x_min, x_max + 0.03, 0.03)  # Minor ticks every 0.03

        # Plot PHID (Density Porosity) with solid red line
        phid_ax.plot(self.df['PHID'], self.df['DEPTH'], 'r-')
        phid_ax.set_xlim(x_min, x_max)
        phid_ax.invert_xaxis()
        self.configure_axis(phid_ax, "DENSITY POROSITY (%)", 'red',
                            major_ticks,
                            [f"{round(tick * 100)}%" for tick in major_ticks])

        # Add minor ticks for PHID axis
        phid_ax.set_xticks(minor_ticks, minor=True)

        # Configure grid for PHID
        phid_ax.grid(True, which='major', linestyle='-', linewidth=2, alpha=0.9)  # Solid major grid
        phid_ax.grid(True, which='minor', linestyle='--', linewidth=1, alpha=0.7)  # Dashed minor grid

        # Plot PHIN (Neutron Porosity) with dashed blue line
        phin_ax.plot(self.df['PHIN'], self.df['DEPTH'], 'b--')
        phin_ax.set_xlim(x_min, x_max)
        phin_ax.invert_xaxis()
        phin_ax.spines["top"].set_position(("axes", 1 + self.AXIS_SPACING))
        self.configure_axis(phin_ax, "NEUTRON POROSITY (%)", 'blue',
                            major_ticks,
                            [f"{round(tick * 100)}%" for tick in major_ticks],
                            linestyle=(0, (5, 5)),
                            label_coord_offset=self.AXIS_SPACING + self.TEXT_SPACING_ABOVE_AXIS)

        # Add minor ticks for PHIN axis
        phin_ax.set_xticks(minor_ticks, minor=True)

        # Plot PHI_AVG_CALC (Average Porosity) with solid black line
        phi_avg_ax.plot(self.df['phi_avg_calc'], self.df['DEPTH'], 'k-', label='Average Porosity')
        phi_avg_ax.set_xlim(x_min, x_max)
        phi_avg_ax.invert_xaxis()
        phi_avg_ax.spines["top"].set_position(("axes", 1 + 2 * self.AXIS_SPACING))
        self.configure_axis(phi_avg_ax, "AVERAGE POROSITY (%)", 'black',
                            major_ticks,
                            [f"{round(tick * 100)}%" for tick in major_ticks],
                            label_coord_offset=2 * self.AXIS_SPACING + self.TEXT_SPACING_ABOVE_AXIS)

        # Add minor ticks for PHI_AVG_CALC axis
        phi_avg_ax.set_xticks(minor_ticks, minor=True)

        # Dynamic scaling for RNML and RLML axes
        rnml_max = self.df['RNML'].max()
        rlml_max = self.df['RLML'].max()
        rnml_scale = 20 if rnml_max <= 20 else 60
        rlml_scale = 20 if rlml_max <= 20 else 60

        # Plot RNML (Dashed Green Line)
        rnml_ax.plot(self.df['RNML'], self.df['DEPTH'], 'g--', label='RNML')
        rnml_ax.set_xlim(0, rnml_scale)
        rnml_ax.spines["top"].set_position(("axes", 1 + 3 * self.AXIS_SPACING))
        self.configure_axis(rnml_ax, "RNML (OHM.M)", 'green',
                            np.arange(0, rnml_scale + 10, 10),
                            [str(int(tick)) for tick in np.arange(0, rnml_scale + 10, 10)],linestyle=(0, (5, 5)),
                            label_coord_offset=3 * self.AXIS_SPACING + self.TEXT_SPACING_ABOVE_AXIS)

        # Plot RLML (Solid Green Line)
        rlml_ax.plot(self.df['RLML'], self.df['DEPTH'], 'g-', label='RLML')
        rlml_ax.set_xlim(0, rlml_scale)
        rlml_ax.spines["top"].set_position(("axes", 1 + 4 * self.AXIS_SPACING))
        self.configure_axis(rlml_ax, "RLML (OHM.M)", 'green',
                            np.arange(0, rlml_scale + 10, 10),
                            [str(int(tick)) for tick in np.arange(0, rlml_scale + 10, 10)],
                            label_coord_offset=4 * self.AXIS_SPACING + self.TEXT_SPACING_ABOVE_AXIS)

        rnml_ax.grid(False)
        rlml_ax.grid(False)

        # Plot Density Correction (new)
        density_corr_ax.plot(self.df['CORR'], self.df['DEPTH'], 'm-', label='Density Correction')
        density_corr_ax.set_xlim(-0.5, 0.5)
        density_corr_ax.spines["top"].set_position(("axes", 1 + 5 * self.AXIS_SPACING))
        self.configure_axis(density_corr_ax, "DENSITY CORR (g/cm³)", 'magenta',
                            np.linspace(-0.5, 0.5, 6),
                            [f"{tick:.1f}" for tick in np.linspace(-0.5, 0.5, 6)],
                            label_coord_offset=5 * self.AXIS_SPACING + self.TEXT_SPACING_ABOVE_AXIS)

        # Shade area where PHID > PHIN (Density > Neutron) to represent sandstone
        mask = self.df['PHID'] > self.df['PHIN']
        phid_ax.fill_betweenx(self.df['DEPTH'], self.df['PHID'], self.df['PHIN'], where=mask, color='yellow', alpha=0.3)
        # Shade areas where RNML > RLML (Mudcake zones)
        mask_mudcake = self.df['RNML'] > self.df['RLML']
        rnml_ax.fill_betweenx(self.df['DEPTH'], self.df['RNML'], self.df['RLML'],
                              where=mask_mudcake, facecolor='brown', alpha=0.5, label='Mudcake Zone')

    def plot_vsh_logs(self):
        # Main axis for Vsh Gamma Ray
        vsh_gr_ax = self.fig.add_axes([0.75, 0.05, 0.2, 0.9], sharey=self.gamma_ray_and_main_ax)
        vsh_sp_ax = vsh_gr_ax.twiny()
        vsh_por_ax = vsh_gr_ax.twiny()

        # Plot Vsh Gamma Ray
        vsh_gr_ax.plot(self.df['Vsh_gamma_ray'], self.df['DEPTH'], 'g-', label='Vsh Gamma Ray')
        vsh_gr_ax.set_xlim(0, 1)
        self.configure_axis(vsh_gr_ax, "Vsh Gamma Ray (%)", 'green', np.linspace(0, 1, 11),
                            [f"{int(tick * 100)}%" for tick in np.linspace(0, 1, 11)])
        # Set y-axis minor ticks
        vsh_gr_ax.set_yticks(np.arange(self.MIN_DEPTH, self.MAX_DEPTH + 2, 2), minor=True)
        vsh_gr_ax.grid(True, which='major', linestyle='-', linewidth=2, alpha=0.9)  # Solid major grid
        vsh_gr_ax.grid(True, which='minor', linestyle='--', linewidth=0.9, alpha=0.7)
        # Plot Vsh SP
        vsh_sp_ax.plot(self.df['Vsh_sp'], self.df['DEPTH'], 'purple', label='Vsh SP')
        vsh_sp_ax.set_xlim(0, 1)
        vsh_sp_ax.spines["top"].set_position(("axes", 1 + self.AXIS_SPACING))
        self.configure_axis(vsh_sp_ax, "Vsh SP (%)", 'purple', np.linspace(0, 1, 11),
                            [f"{int(tick * 100)}%" for tick in np.linspace(0, 1, 11)],
                            label_coord_offset=self.AXIS_SPACING + self.TEXT_SPACING_ABOVE_AXIS)

        # Plot Vsh Porosity
        vsh_por_ax.plot(self.df['Vsh_porosity'], self.df['DEPTH'], 'orange', label='Vsh Porosity')
        vsh_por_ax.set_xlim(0, 1)
        vsh_por_ax.spines["top"].set_position(("axes", 1 + 2 * self.AXIS_SPACING))
        self.configure_axis(vsh_por_ax, "Vsh Porosity (%)", 'orange', np.linspace(0, 1, 11),
                            [f"{int(tick * 100)}%" for tick in np.linspace(0, 1, 11)],
                            label_coord_offset=2 * self.AXIS_SPACING + self.TEXT_SPACING_ABOVE_AXIS)


    def plot_all(self):
        self.plot_main_log()
        self.plot_resistivity_logs()
        self.plot_porosity_logs()
        self.plot_vsh_logs()  # New Vsh plots
        plt.show()
