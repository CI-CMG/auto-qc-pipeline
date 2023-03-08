#! /bin/bash

set -ex

if [[ -z "${AUTO_QC_HOME}" ]]
then
  echo "Error - AUTO_QC_HOME not set"
  exit 2
fi

wd=$(pwd)

cd "$AUTO_QC_HOME"

cd data

if [ ! -f EN_bgcheck_info.nc ]
then
  wget --quiet http://www.metoffice.gov.uk/hadobs/en4/data/EN_bgcheck_info.nc
fi

if [ ! -f temperature_seasonal_5deg.nc ]
then
  wget --quiet https://www.ncei.noaa.gov/data/oceans/woa/WOA09/NetCDFdata/temperature_seasonal_5deg.nc
fi

if [ ! -f etopo5.nc ]
then
  wget --quiet "https://pae-paha.pacioos.hawaii.edu/thredds/ncss/etopo5?var=ROSE&disableLLSubset=on&disableProjSubset=on&horizStride=1&addLatLon=true" -O etopo5.nc
fi

if [ ! -f woa13_decav_t13_5dv2.nc ]
then
  wget --quiet https://www.ncei.noaa.gov/data/oceans/woa/WOA13/DATAv2/sea_water_temperature/netcdf/decav/5deg/woa13_decav_t13_5dv2.nc
fi

if [ ! -f woa13_decav_t14_5dv2.nc ]
then
  wget --quiet https://www.ncei.noaa.gov/data/oceans/woa/WOA13/DATAv2/sea_water_temperature/netcdf/decav/5deg/woa13_decav_t14_5dv2.nc
fi

if [ ! -f woa13_decav_t15_5dv2.nc ]
then
  wget --quiet https://www.ncei.noaa.gov/data/oceans/woa/WOA13/DATAv2/sea_water_temperature/netcdf/decav/5deg/woa13_decav_t15_5dv2.nc
fi

if [ ! -f woa13_decav_t16_5dv2.nc ]
then
  wget --quiet https://www.ncei.noaa.gov/data/oceans/woa/WOA13/DATAv2/sea_water_temperature/netcdf/decav/5deg/woa13_decav_t16_5dv2.nc
fi

if [ ! -f woa13_decav_s13_5dv2.nc ]
then
  wget --quiet https://www.ncei.noaa.gov/data/oceans/woa/WOA13/DATAv2/salinity/netcdf/decav/5deg/woa13_decav_s13_5dv2.nc
fi

if [ ! -f woa13_decav_s14_5dv2.nc ]
then
  wget --quiet https://www.ncei.noaa.gov/data/oceans/woa/WOA13/DATAv2/salinity/netcdf/decav/5deg/woa13_decav_s14_5dv2.nc
fi

if [ ! -f woa13_decav_s15_5dv2.nc ]
then
  wget --quiet https://www.ncei.noaa.gov/data/oceans/woa/WOA13/DATAv2/salinity/netcdf/decav/5deg/woa13_decav_s15_5dv2.nc
fi

if [ ! -f woa13_decav_s16_5dv2.nc ]
then
  wget --quiet https://www.ncei.noaa.gov/data/oceans/woa/WOA13/DATAv2/salinity/netcdf/decav/5deg/woa13_decav_s16_5dv2.nc
fi

if [ ! -f woa13_00_025.nc ]
then
  wget --quiet ftp://ftp.aoml.noaa.gov/phod/pub/bringas/XBT/AQC/AOML_AQC_2018/data_center/woa13_00_025.nc
fi

if [ ! -f climatological_t_median_and_amd_for_aqc.nc ]
then
  wget --quiet https://s3-us-west-2.amazonaws.com/autoqc/climatological_t_median_and_amd_for_aqc.nc
fi

if [ ! -f GRID_MIN_MAX.nc ]
then
  wget --quiet https://auto-qc-data.s3.us-west-2.amazonaws.com/GRID_MIN_MAX.nc
fi

if [ ! -f info_DGG4H6.mat ]
then
  wget --quiet https://auto-qc-data.s3.us-west-2.amazonaws.com/info_DGG4H6.mat
fi

if [ ! -f TEMP_MIN_MAX.nc ]
then
  wget --quiet https://auto-qc-data.s3.us-west-2.amazonaws.com/TEMP_MIN_MAX.nc
fi

if [ ! -f global_mean_median_quartiles_medcouple_smoothed.nc ]
then
  wget --quiet https://auto-qc-data.s3.us-west-2.amazonaws.com/global_mean_median_quartiles_medcouple_smoothed.nc
fi

cd "$wd"
