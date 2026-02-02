import copernicusmarine

import os
import numpy as np
import cmocean.cm as cmo



shortname_dict = {
    'monthly_wind_stress': 'cmems_obs-wind_glo_phy_my_l4_P1M',
    'daily_winds': 'cmems_obs-wind_glo_phy_my_l4_P1M',
    'total_currents_glob': 'cmems_obs-mob_glo_phy-cur_my_0.25deg_P1D-m',
    'phys_currents': 'cmems_obs-mob_glo_phy-cur_my_0.25deg_P1D-m'
}

full_details = {
    'monthly_wind_stress': {
        'file_name': 'cmems_mod_setio_winds_monthly.nc',
        'prod_name': 'Global Ocean Monthly Mean Sea Surface Wind and Stress',
        'cmems_id': shortname_dict['monthly_wind_stress'],
        'variable': ['eastward_stress', 'northward_stress'],
        'plot_title': 'Mean surface wind stress in month {} (with interannual variability contours)',
        'contour_type': 'inter-annual variability',
        'clabel_fmt': "%.2f",
        'save_name': 'Windstress_month',
        'cmap': cmo.speed,
    },
    'Ekman_currents_glob': {
        'file_name': 'cmems_setio_currents.nc',
        'prod_name': 'Ekman Surface Currents',
        'cmems_id': shortname_dict['total_currents_glob'],
        'variable': ['ue', 've'],
        'plot_title': 'Mean surface Ekman currents in month {} (with daily variability contours)',
        'contour_type': 'daily variability',
        'clabel_fmt': "%.2f",
        'save_name': 'EkmanGlobCurrents_month',
        'cmap': cmo.haline,
    },
    'geo_currents_glob': {
        'file_name': 'cmems_setio_currents.nc',
        'prod_name': 'Geostrophic Surface Currents',
        'cmems_id': shortname_dict['total_currents_glob'],
        'variable': ['ugos', 'vgos'],
        'plot_title': 'Mean geostrophic surface currents in month {} (with daily variability contours)',
        'contour_type': 'daily variability',
        'clabel_fmt': "%.2f",
        'save_name': 'GeoCurrents_month',
        'cmap': cmo.dense,
    },
    'currents_model': {
        'file_name': 'cmems_mod_setio_currents.nc',
        'prod_name': 'Modelled Surface Currents',
        'cmems_id': shortname_dict['phys_currents'],
        'variable': ['uo', 'vo'],
        'plot_title': 'Mean modelled surface currents in month {} (with daily variability contours)',
        'contour_type': 'daily variability',
        'clabel_fmt': "%.2f",
        'save_name': 'ModelledCurrents_month',
        'cmap': cmo.matter,
    },
}


def get_cmems_details(short_name):
    """
    Retrieve CMEMS dataset details based on short name.

    Parameters:
        short_name (str): Dataset short name.

    Returns:
        dict: Dataset details including file name, product name, variables, etc.
    """
    if short_name in full_details:
        return full_details[short_name]
    else:
        raise ValueError(f"Dataset with short name '{short_name}' not found.")






def download_cmems(short_name, save_path, lon_bounds, lat_bounds, time_bounds=None, ds_vars=None, depth_range=[0,0]):
    """
    Download data from CMEMS with basic checks and warnings.

    Parameters:
        short_name (str): Dataset short name.
        save_path (str): Path to save the downloaded file.
        lon_bounds (tuple): Longitude bounds (min, max).
        lat_bounds (tuple): Latitude bounds (min, max).
        time_bounds (tuple, optional): Time bounds (start, end).
        ds_vars (list, optional): Variables to download.
        min_depth (float, optional): Minimum depth.
        max_depth (float, optional): Maximum depth.

    Returns:
        None
    """
    # Check filename exists
    if os.path.isfile(save_path):
        print(f"Warning: file already exists!")
        proceed = input("Do you want to overwrite, save new file, or cancel? (ow/new/cancel): ").strip().lower()
        if proceed == 'ow':
            print('Deleting old file')
            os.remove(save_path)
        elif proceed == 'new':
            print('Adding a new file')
        elif proceed == 'cancel':
            print("Download cancelled.")
            return
        else: 
            print('Response unknown, attempt cancelled.')
            return
    
    # Check longitude and latitude bounds
    if lon_bounds[0] < -180 or lon_bounds[1] > 180:
        raise ValueError("Longitude bounds must be within -180 to 180.")
    if lat_bounds[0] < -90 or lat_bounds[1] > 90:
        raise ValueError("Latitude bounds must be within -90 to 90.")

    # Check if variables are provided
    if not ds_vars or not isinstance(ds_vars, list):
        print('No variables selected for download, requesting all variables in dataset.')
        # raise ValueError("You must provide a list of variables to download.")

    # Estimate dataset size
    lon_range = abs(lon_bounds[1] - lon_bounds[0])
    lat_range = abs(lat_bounds[1] - lat_bounds[0])
    time_range = 1 if not time_bounds else (np.datetime64(time_bounds[1]) - np.datetime64(time_bounds[0])).astype('timedelta64[D]').item().days

    estimated_size = lon_range * lat_range * time_range * len(ds_vars) * 0.0001  # Approximation in MB

    if estimated_size > 500:  # Arbitrary threshold for large downloads
        print(f"Warning: The estimated download size is {estimated_size:.2f} MB. This might take a long time.")
        proceed = input("Do you want to continue? (yes/no): ").strip().lower()
        if proceed != 'yes':
            print("Download cancelled.")
            return

    # Perform the download
    try:
        cp_obj = copernicusmarine.subset(
                        dataset_id=shortname_dict[short_name],
                        variables=ds_vars,
                        minimum_longitude=lon_bounds[0],
                        maximum_longitude=lon_bounds[1],
                        minimum_latitude=lat_bounds[0],
                        maximum_latitude=lat_bounds[1],
                        start_datetime=time_bounds[0] if time_bounds else None,
                        end_datetime=time_bounds[1] if time_bounds else None,
                        minimum_depth=depth_range[0],
                        maximum_depth=depth_range[1],
                        output_filename=os.path.basename(save_path),
                        output_directory=os.path.dirname(save_path)
        )
        print(f"Download complete. File saved to {save_path}")
        return cp_obj
    except Exception as e:
        print(f"An error occurred during download: {e}")