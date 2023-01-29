from eipiphany_core.framework.base.filter import Filter
from profile_filter import ProfileFilter


class PathologicalProfilesFilter(Filter):

  def __init__(self):
    self.__filter = ProfileFilter()

  # todo incorporate this?
  #
  #   # encode temperature error codes into truth array
  #   truth = encodeTruth(profile)
  #   p['truth'] = main.pack_array(truth)
  #
  #   # extract country code
  #   country = profile.primary_header['Country code']
  #
  #   # originator cruise
  #   orig_cruise = profile.originator_cruise()
  #
  #   # keep tabs on how many good and how many bad profiles have been added to db
  #   # nowire == index of first wire break level
  #   wireqc = qctests.CSIRO_wire_break.test(profile, {})
  #   try:
  #     nowire = list(wireqc).index(True)
  #   except:
  #     nowire = len(truth)
  #   # flag only counts if its before the wire break:
  #   flagged = dbutils.summarize_truth(truth[0:nowire])
  #   if flagged:
  #     bad += 1
  #   else:
  #     good += 1
  #
  #   query = "INSERT INTO " + dbtable + " (raw, truth, uid, year, month, day, time, lat, long, country, cruise, ocruise, probe, flagged) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?);"
  #   values = (p['raw'], p['truth'], p['uid'], p['year'], p['month'], p['day'], p['time'], p['latitude'], p['longitude'], country, p['cruise'], orig_cruise, p['probe_type'], int(flagged))
  #   main.dbinteract(query, values, targetdb=outfile)
  #   if profile.is_last_profile_in_file(fid) == True:
  #     break
  #
  # conn.commit()
  # print('number of clean profiles written:', good)
  # print('number of flagged profiles written:', bad)
  # print('total number of profiles written:', good+bad)
  def filter(self, exchange):
    auto_qc_test_message = exchange.body
    return self.__filter.assess_profile(auto_qc_test_message.profile)