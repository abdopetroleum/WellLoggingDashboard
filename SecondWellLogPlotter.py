import matplotlib.pyplot as plt
import numpy as np

class SecondWellLogPlotter:
    def __init__(self, df,sp_shift):
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
        self.gamma_ray_and_main_ax = self.fig.add_axes([0, 0.05, 0.3, 0.9])
        bit_size_ax = self.gamma_ray_and_main_ax.twiny()
        caliper_ax = self.gamma_ray_and_main_ax.twiny()
        sp_ax = self.gamma_ray_and_main_ax.twiny()  # New SP log axis

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
        self.gamma_ray_and_main_ax.grid(True, which='minor', linestyle='--', linewidth=0.9, alpha=0.7)  # Minor grid

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
        sp_ax.set_xlim(self.df['SP'].min(), self.df['SP'].min() + 20 * 10)  # Original SP-based limits
        sp_ax.spines["top"].set_position(("axes", 1 + 3 * self.AXIS_SPACING))

        # Enable X-ticks for SP axis
        sp_xticks = np.arange(self.df['SP'].min(), self.df['SP'].min() + 20 * 10 + 1,
                              20)  # Adjust spacing to match SP ticks
        sp_ax.tick_params(axis='x', which='both', top=True, labeltop=True)

        self.configure_axis(sp_ax, "SP LOG (20 mV)", 'purple', sp_xticks, [str(int(tick)) for tick in sp_xticks],
                            label_coord_offset=3 * self.AXIS_SPACING + self.TEXT_SPACING_ABOVE_AXIS)
        sp_ax.grid(False)

    def plot_saturation_logs(self):
        # Main axis for Sw
        saturation_ax = self.fig.add_axes([0.35, 0.05, 0.3, 0.9], sharey=self.gamma_ray_and_main_ax)
        sxo_ax = saturation_ax.twiny()  # For Sxo
        bv_w_ax = saturation_ax.twiny()  # For BVW

        # Plot Sw
        saturation_ax.plot(self.df['Sw'], self.df['DEPTH'], 'b-', label='Sw')
        saturation_ax.set_xlim(-0.2, 1.2)
        self.configure_axis(saturation_ax, "Sw (%)", 'blue', np.arange(-0.2, 1.3, 0.2),
                            [f"{int(t * 100)}%" for t in np.arange(-0.2, 1.3, 0.2)])
        saturation_ax.grid(True, which='major', linestyle='-', linewidth=1.5, alpha=0.8)
        saturation_ax.grid(True, which='minor', linestyle='--', linewidth=0.9, alpha=0.7)
        # Plot Sxo (Flushed Zone Saturation)
        sxo_ax.plot(self.df['Sxo'], self.df['DEPTH'], 'r--', label='Sxo')
        sxo_ax.set_xlim(-0.2, 1.2)
        sxo_ax.spines["top"].set_position(("axes", 1 + self.AXIS_SPACING))
        self.configure_axis(sxo_ax, "Sxo (%)", 'red', np.arange(-0.2, 1.3, 0.2),
                            [f"{int(t * 100)}%" for t in np.arange(-0.2, 1.3, 0.2)],
                            label_coord_offset=self.AXIS_SPACING + self.TEXT_SPACING_ABOVE_AXIS)
        sxo_ax.grid(False)

        # Plot BVW
        bv_w_ax.plot(self.df['Bvw'], self.df['DEPTH'], 'purple', label='BVW')
        bv_w_ax.set_xlim(0, 0.5)
        bv_w_ax.spines["top"].set_position(("axes", 1 + 2 * self.AXIS_SPACING))
        self.configure_axis(bv_w_ax, "BVW (%)", 'purple', np.arange(0, 0.55, 0.05),
                            [f"{int(tick * 100)}%" for tick in np.arange(0, 0.55, 0.05)],
                            label_coord_offset=2 * self.AXIS_SPACING + self.TEXT_SPACING_ABOVE_AXIS)
        bv_w_ax.grid(False)

    def plot_mhi_log(self):
        mhi_ax =self.fig.add_axes([0.7, 0.05, 0.1, 0.9], sharey=self.gamma_ray_and_main_ax)
        mhi_ax.plot(self.df['MHI'], self.df['DEPTH'], 'k-')
        mhi_ax.set_xlim(0, 1.2)
        mhi_ax.invert_yaxis()
        self.configure_axis(mhi_ax, "MHI", 'black', np.arange(0, 1.3, 0.2), [f"{tick:.1f}" for tick in np.arange(0, 1.3, 0.2)])
        mhi_ax.grid(True, which='major', linestyle='-', linewidth=2, alpha=0.9)
        mhi_ax.grid(True, which='minor', linestyle='--', linewidth=0.9, alpha=0.7)

    def plot_delta_bvw_log(self):
        bvw_ax = self.fig.add_axes([0.85, 0.05, 0.1, 0.9], sharey=self.gamma_ray_and_main_ax)

        # Plot Delta BVW
        bvw_ax.plot(self.df['delta_Bvw'], self.df['DEPTH'], color='#008080', label='Delta BVW')
        bvw_ax.set_xlim(-0.02, 0.02)  # Updated x-axis range
        bvw_ax.invert_yaxis()

        # Configure the axis with 10 evenly spaced ticks
        delta_bvw_ticks = np.linspace(-0.02, 0.02, 5)
        self.configure_axis(
            bvw_ax,
            "Delta BVW",
            '#008080',
            delta_bvw_ticks,
            [f"{tick:.3f}" for tick in delta_bvw_ticks]
        )
        bvw_ax.grid(True, which='major', linestyle='-', linewidth=2, alpha=0.9)
        bvw_ax.grid(True, which='minor', linestyle='--', linewidth=0.9, alpha=0.7)

    def plot_all(self):
        self.plot_main_log()
        self.plot_saturation_logs()
        self.plot_mhi_log()
        self.plot_delta_bvw_log()
        plt.show()
