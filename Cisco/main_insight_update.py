from modules import update_insight_objects as insight_object


data = r'/Users/mehdi/Ariana/Cisco/1/cisco/cisco_ipbb/cisco_ipbb_version.csv'
insight_username = 'user'
insight_password = 'pass'

nwg = insight_object.NetworkInsightCreateUpdate(insight_username=insight_username, insight_password=insight_password)

insight_object_name = "Cisco IPBB"

nwg.get_object_entires(insight_object_name)
nwg.update_or_create_insight(data)

