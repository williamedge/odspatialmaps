import os
import matplotlib.pyplot as plt
import cartopy
import cartopy.crs as ccrs


def plot_monthly_data(ds, details_dict, save_dir, scale=7, thin=6):
    # Take the July mean of the Ekman currents
    p_vars = details_dict['variable']

    for p_months in range(1,13):

        ds_month = ds[p_vars].sel(time=ds.time.dt.month == p_months).mean(dim='time').squeeze()

        # Compute the inter-annual variability
        ds_std = ds[p_vars].sel(time=ds.time.dt.month == p_months).std(dim='time').squeeze()
        plt_std = (ds_std[p_vars[0]]**2 + ds_std[p_vars[1]]**2)**0.5
        plt_smoothed = plt_std.rolling(latitude=4, longitude=4, center=True).mean()
        
        xl = ds_month.longitude.max().values - ds_month.longitude.min().values
        yl = ds_month.latitude.max().values - ds_month.latitude.min().values

        fig, ax = plt.subplots(figsize=(16, 16*yl/xl), subplot_kw={'projection': ccrs.PlateCarree()})

        ax.add_feature(cartopy.feature.LAND, facecolor='w', zorder=2, edgecolor='grey', linewidths=1, alpha=1)
        ax.add_feature(cartopy.feature.LAND, facecolor='olive', alpha=0.1, zorder=3, edgecolor=None, linewidths=0)

        speed = (ds_month[p_vars[0]]**2 + ds_month[p_vars[1]]**2)**0.5
        speed.plot.pcolormesh(ax=ax, cmap=details_dict['cmap'], shading='auto', alpha=0.8, cbar_kwargs={'pad':0.01, 'shrink':0.8})
        
        contour = plt_smoothed.plot.contour(ax=ax, levels=6, colors='darkslategrey', linewidths=1, linestyles='-')
        ax.clabel(contour, inline=True, fontsize=10, fmt=details_dict['clabel_fmt'])

        ds_month_thin = ds_month.isel(latitude=slice(thin//2, None, thin),
                                    longitude=slice(thin//2, None, thin))
        plt.quiver(
            ds_month_thin.longitude.values,
            ds_month_thin.latitude.values,
            ds_month_thin[p_vars[0]].values,
            ds_month_thin[p_vars[1]].values,
            scale=scale,
            width=0.0014,
            color='black',
            alpha=0.7)

        plt.xlim(ds.longitude.min(), ds.longitude.max())
        plt.ylim(ds.latitude.min(), ds.latitude.max())

        plt.title(details_dict['plot_title'].format(p_months), fontsize=16)

        gl = ax.gridlines(draw_labels=True)
        gl.xlines = False
        gl.ylines = False
        gl.top_labels = False
        gl.right_labels = False

        plt.scatter(123.3744, -13.74942, c='orange', s=60, edgecolor='k', zorder=5, linewidths=2)

        plt.text(0.1, 0.06, 'Product: {}, Dataset ID: {}, Data source: Copernicus Marine Service \nVariables shown: {}, Date range: {}, Contours shown: {}\nSaved to: {}'\
                    .format(details_dict['prod_name'],\
                            details_dict['cmems_id'],\
                            details_dict['variable'],\
                            (str(ds.time.min().values.astype('datetime64[M]')), str(ds.time.max().values.astype('datetime64[M]'))),\
                            details_dict['contour_type'],\
                            save_dir),\
                        fontsize=10, transform=fig.transFigure, ha='left', linespacing=1.5)

        fmt = 'png'
        full_save = os.path.join(save_dir, details_dict['save_name'] + str(int(p_months)) + '.' + fmt)
        fig.savefig(full_save, format=fmt, transparent=False,\
                        bbox_inches='tight', pad_inches=0.06, dpi=300)
        plt.close(fig)
        
        
        
def plot_monthly_eke(ds, details_dict, save_dir):
    # Take the July mean of the Ekman currents
    p_vars = details_dict['variable']

    for p_months in range(1,13):

        ds_month = ds[p_vars].sel(time=ds.time.dt.month == p_months).mean(dim='time').squeeze()

        # Compute the inter-annual variability
        ds_std = ds[p_vars].sel(time=ds.time.dt.month == p_months).std(dim='time').squeeze()
        plt_std = (ds_std[p_vars[0]]**2 + ds_std[p_vars[1]]**2)**0.5
        plt_smoothed = plt_std.rolling(latitude=4, longitude=4, center=True).mean()
        
        xl = ds_month.longitude.max().values - ds_month.longitude.min().values
        yl = ds_month.latitude.max().values - ds_month.latitude.min().values

        fig, ax = plt.subplots(figsize=(16, 16*yl/xl), subplot_kw={'projection': ccrs.PlateCarree()})

        ax.add_feature(cartopy.feature.LAND, facecolor='w', zorder=2, edgecolor='grey', linewidths=1, alpha=1)
        ax.add_feature(cartopy.feature.LAND, facecolor='olive', alpha=0.1, zorder=3, edgecolor=None, linewidths=0)

        plt_std.plot.pcolormesh(ax=ax, cmap=details_dict['cmap'], shading='auto', alpha=0.8, vmin=0, vmax=0.6, cbar_kwargs={'pad':0.01, 'shrink':0.8})
        
        contour = plt_smoothed.plot.contour(ax=ax, levels=6, colors='darkslategrey', linewidths=1, linestyles='-')
        ax.clabel(contour, inline=True, fontsize=10, fmt=details_dict['clabel_fmt'])

        plt.xlim(ds.longitude.min(), ds.longitude.max())
        plt.ylim(ds.latitude.min(), ds.latitude.max())

        plt.title('Mean Eddy Kinetic Energy in month {}'.format(p_months), fontsize=16)

        gl = ax.gridlines(draw_labels=True)
        gl.xlines = False
        gl.ylines = False
        gl.top_labels = False
        gl.right_labels = False

        plt.scatter(123.3744, -13.74942, c='orange', s=60, edgecolor='k', zorder=5, linewidths=2)

        plt.text(0.1, 0.06, 'Product: {}, Dataset ID: {}, Data source: Copernicus Marine Service \nVariables shown: {}, Date range: {}, Contours shown: {}\nSaved to: {}'\
                    .format(details_dict['prod_name'],\
                            details_dict['cmems_id'],\
                            details_dict['variable'],\
                            (str(ds.time.min().values.astype('datetime64[M]')), str(ds.time.max().values.astype('datetime64[M]'))),\
                            details_dict['contour_type'],\
                            save_dir),\
                        fontsize=10, transform=fig.transFigure, ha='left', linespacing=1.5)

        fmt = 'png'
        full_save = os.path.join(save_dir, 'EKEModelled_month' + str(int(p_months)) + '.' + fmt)
        fig.savefig(full_save, format=fmt, transparent=False,\
                        bbox_inches='tight', pad_inches=0.06, dpi=300)
        plt.close(fig)