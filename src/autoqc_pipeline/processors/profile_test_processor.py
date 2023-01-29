import os

import qctests.AOML_climatology_test as AOML_climatology_test
import qctests.AOML_constant as AOML_constant
import qctests.AOML_gradient as AOML_gradient
import qctests.AOML_gross as AOML_gross
import qctests.AOML_spike as AOML_spike
import qctests.Argo_global_range_check as Argo_global_range_check
import qctests.Argo_gradient_test as Argo_gradient_test
import qctests.Argo_impossible_date_test as Argo_impossible_date_test
import qctests.Argo_impossible_location_test as Argo_impossible_location_test
import qctests.Argo_pressure_increasing_test as Argo_pressure_increasing_test
import qctests.Argo_regional_range_test as Argo_regional_range_test
import qctests.Argo_spike_test as Argo_spike_test
import qctests.CoTeDe_anomaly_detection as CoTeDe_anomaly_detection
import qctests.CoTeDe_Argo_density_inversion as CoTeDe_Argo_density_inversion
import qctests.CoTeDe_digit_roll_over as CoTeDe_digit_roll_over
import qctests.CoTeDe_fuzzy_logic as CoTeDe_fuzzy_logic
import qctests.CoTeDe_gradient as CoTeDe_gradient
import qctests.CoTeDe_GTSPP_global_range as CoTeDe_GTSPP_global_range
import qctests.CoTeDe_GTSPP_gradient as CoTeDe_GTSPP_gradient
import qctests.CoTeDe_GTSPP_profile_envelop as CoTeDe_GTSPP_profile_envelop
import qctests.CoTeDe_GTSPP_spike_check as CoTeDe_GTSPP_spike_check
import qctests.CoTeDe_GTSPP_WOA_normbias as CoTeDe_GTSPP_WOA_normbias
import qctests.CoTeDe_location_at_sea_test as CoTeDe_location_at_sea_test
import qctests.CoTeDe_Morello2014 as CoTeDe_Morello2014
import qctests.CoTeDe_rate_of_change as CoTeDe_rate_of_change
import qctests.CoTeDe_spike as CoTeDe_spike
import qctests.CoTeDe_tukey53H as CoTeDe_tukey53H
import qctests.CoTeDe_tukey53H_norm as CoTeDe_tukey53H_norm
import qctests.CoTeDe_WOA_normbias as CoTeDe_WOA_normbias
import qctests.CSIRO_constant_bottom as CSIRO_constant_bottom
import qctests.CSIRO_depth as CSIRO_depth
import qctests.CSIRO_long_gradient as CSIRO_long_gradient
import qctests.CSIRO_short_gradient as CSIRO_short_gradient
import qctests.CSIRO_surface_spikes as CSIRO_surface_spikes
import qctests.CSIRO_wire_break as CSIRO_wire_break
import qctests.EN_background_available_check as EN_background_available_check
import qctests.EN_background_check as EN_background_check
import qctests.EN_constant_value_check as EN_constant_value_check
import qctests.EN_increasing_depth_check as EN_increasing_depth_check
import qctests.EN_range_check as EN_range_check
import qctests.EN_spike_and_step_check as EN_spike_and_step_check
import qctests.EN_spike_and_step_suspect as EN_spike_and_step_suspect
import qctests.EN_stability_check as EN_stability_check
import qctests.EN_std_lev_bkg_and_buddy_check as EN_std_lev_bkg_and_buddy_check
import qctests.EN_track_check as EN_track_check
import qctests.ICDC_aqc_01_level_order as ICDC_aqc_01_level_order
import qctests.ICDC_aqc_02_crude_range as ICDC_aqc_02_crude_range
import qctests.ICDC_aqc_04_max_obs_depth as ICDC_aqc_04_max_obs_depth
import qctests.ICDC_aqc_05_stuck_value as ICDC_aqc_05_stuck_value
import qctests.ICDC_aqc_06_n_temperature_extrema as ICDC_aqc_06_n_temperature_extrema
import qctests.ICDC_aqc_07_spike_check as ICDC_aqc_07_spike_check
import qctests.ICDC_aqc_08_gradient_check as ICDC_aqc_08_gradient_check
import qctests.ICDC_aqc_09_local_climatology_check as ICDC_aqc_09_local_climatology_check
import qctests.ICDC_aqc_10_local_climatology_check as ICDC_aqc_10_local_climatology_check
import qctests.IQUOD_bottom as IQUOD_bottom
import qctests.IQuOD_gross_range_check as IQuOD_gross_range_check
import qctests.loose_location_at_sea as loose_location_at_sea
import qctests.minmax as minmax
import qctests.WOD_gradient_check as WOD_gradient_check
import qctests.WOD_range_check as WOD_range_check
from eipiphany_core.framework.base.processor import Processor


class TestInfo(object):
  def __init__(self, name, module, has_parameters = False):
    self.name = name
    self.__module = module
    self.__has_parameters = has_parameters

  def load_parameters(self, parameter_store):
    if self.__has_parameters:
      self.__module.loadParameters(parameter_store)

  def test(self, profile, parameter_store):
    return self.__module.test(profile, parameter_store)


tests = [
  TestInfo('AOML_climatology_test', AOML_climatology_test),
  TestInfo('AOML_constant', AOML_constant),
  TestInfo('AOML_gradient', AOML_gradient),
  TestInfo('AOML_gross', AOML_gross),
  TestInfo('AOML_spike', AOML_spike),
  TestInfo('Argo_global_range_check', Argo_global_range_check),
  TestInfo('Argo_gradient_test', Argo_gradient_test),
  TestInfo('Argo_impossible_date_test', Argo_impossible_date_test),
  TestInfo('Argo_impossible_location_test', Argo_impossible_location_test),
  TestInfo('Argo_pressure_increasing_test', Argo_pressure_increasing_test),
  TestInfo('Argo_regional_range_test', Argo_regional_range_test),
  TestInfo('Argo_spike_test', Argo_spike_test),
  TestInfo('CoTeDe_anomaly_detection', CoTeDe_anomaly_detection),
  TestInfo('CoTeDe_Argo_density_inversion', CoTeDe_Argo_density_inversion),
  TestInfo('CoTeDe_digit_roll_over', CoTeDe_digit_roll_over),
  TestInfo('CoTeDe_fuzzy_logic', CoTeDe_fuzzy_logic),
  TestInfo('CoTeDe_gradient', CoTeDe_gradient),
  TestInfo('CoTeDe_GTSPP_global_range', CoTeDe_GTSPP_global_range),
  TestInfo('CoTeDe_GTSPP_gradient', CoTeDe_GTSPP_gradient),
  TestInfo('CoTeDe_GTSPP_profile_envelop', CoTeDe_GTSPP_profile_envelop),
  TestInfo('CoTeDe_GTSPP_spike_check', CoTeDe_GTSPP_spike_check),
  TestInfo('CoTeDe_GTSPP_WOA_normbias', CoTeDe_GTSPP_WOA_normbias),
  TestInfo('CoTeDe_location_at_sea_test', CoTeDe_location_at_sea_test),
  TestInfo('CoTeDe_Morello2014', CoTeDe_Morello2014),
  TestInfo('CoTeDe_rate_of_change', CoTeDe_rate_of_change),
  TestInfo('CoTeDe_spike', CoTeDe_spike),
  TestInfo('CoTeDe_tukey53H', CoTeDe_tukey53H),
  TestInfo('CoTeDe_tukey53H_norm', CoTeDe_tukey53H_norm),
  TestInfo('CoTeDe_WOA_normbias', CoTeDe_WOA_normbias),
  TestInfo('CSIRO_constant_bottom', CSIRO_constant_bottom),
  TestInfo('CSIRO_depth', CSIRO_depth),
  TestInfo('CSIRO_long_gradient', CSIRO_long_gradient),
  TestInfo('CSIRO_short_gradient', CSIRO_short_gradient),
  TestInfo('CSIRO_surface_spikes', CSIRO_surface_spikes),
  TestInfo('CSIRO_wire_break', CSIRO_wire_break),
  TestInfo('EN_background_available_check', EN_background_available_check, has_parameters=True),
  TestInfo('EN_background_check', EN_background_check),
  TestInfo('EN_constant_value_check', EN_constant_value_check),
  TestInfo('EN_increasing_depth_check', EN_increasing_depth_check),
  TestInfo('EN_range_check', EN_range_check),
  TestInfo('EN_spike_and_step_check', EN_spike_and_step_check),
  TestInfo('EN_spike_and_step_suspect', EN_spike_and_step_suspect),
  TestInfo('EN_stability_check', EN_stability_check),
  TestInfo('EN_std_lev_bkg_and_buddy_check', EN_std_lev_bkg_and_buddy_check),
  TestInfo('EN_track_check', EN_track_check),
  TestInfo('ICDC_aqc_01_level_order', ICDC_aqc_01_level_order),
  TestInfo('ICDC_aqc_02_crude_range', ICDC_aqc_02_crude_range),
  TestInfo('ICDC_aqc_04_max_obs_depth', ICDC_aqc_04_max_obs_depth),
  TestInfo('ICDC_aqc_05_stuck_value', ICDC_aqc_05_stuck_value),
  TestInfo('ICDC_aqc_06_n_temperature_extrema', ICDC_aqc_06_n_temperature_extrema),
  TestInfo('ICDC_aqc_07_spike_check', ICDC_aqc_07_spike_check),
  TestInfo('ICDC_aqc_08_gradient_check', ICDC_aqc_08_gradient_check),
  TestInfo('ICDC_aqc_09_local_climatology_check', ICDC_aqc_09_local_climatology_check),
  TestInfo('ICDC_aqc_10_local_climatology_check', ICDC_aqc_10_local_climatology_check),
  TestInfo('IQUOD_bottom', IQUOD_bottom),
  TestInfo('IQuOD_gross_range_check', IQuOD_gross_range_check),
  TestInfo('loose_location_at_sea', loose_location_at_sea),
  TestInfo('minmax', minmax),
  TestInfo('WOD_gradient_check', WOD_gradient_check),
  TestInfo('WOD_range_check', WOD_range_check),
]



class ProfileTestProcessor(Processor):

  def __init__(self, auto_qc_home, filter):
    self.__parameter_store = {}
    self.__auto_qc_home = auto_qc_home
    self.__filter = filter
    cwd = os.getcwd()
    try:
      os.chdir(auto_qc_home)
      for test in tests:
        test.load_parameters(self.__parameter_store)
    finally:
      os.chdir(cwd)


  def process(self, exchange):
    test_message = exchange.body
    if self.__filter.filter(exchange):
      profile = test_message.profile
      auto_qc_profile_test_result = test_message.profile_test_result
      cwd = os.getcwd()
      try:
        os.chdir(self.__auto_qc_home)
        for test in tests:
          level_results = test.test(profile, self.__parameter_store).to_list()
          for depth in range(len(level_results)):
            if level_results[depth]:
              auto_qc_profile_test_result.profile_failures.add(test.name)
              auto_qc_profile_test_result.depth_failures[depth].add(test.name)
      finally:
        os.chdir(cwd)
    else:
      test_message.profile_test_result.skipped = True