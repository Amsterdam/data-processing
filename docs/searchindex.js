Search.setIndex({docnames:["_modules/datapunt_processing","_modules/datapunt_processing.extract","_modules/datapunt_processing.helpers","_modules/datapunt_processing.load","_modules/datapunt_processing.transform","_modules/datapunt_processing.transform.enrichment","_modules/datapunt_processing.transform.geospatial","_modules/datapunt_processing.transform.preprocessing","_modules/modules","extract/download_from_api_brk","extract/download_from_api_kvk","extract/download_from_api_tellus","extract/download_from_api_with_authentication","extract/download_from_catalog","extract/download_from_objectstore","extract/download_from_wfs","index","introduction","license","load/load_file_to_ckan","load/load_file_to_objectstore","load/load_wfs_into_postgres","load/load_xls_into_postgres","modules","transform/enrichment/add_knmi_data","transform/enrichment/add_public_events","transform/geospatial/api_clean_BAG_address_NED","transform/geospatial/api_get_area_codes_from_latlon","transform/geospatial/api_get_nearest_address_from_coordinate","transform/geospatial/divide_bbox_amsterdam_in_quadrants","transform/geospatial/postgres_add_areas_from_coordinates","transform/geospatial/rd_to_wgs84"],envversion:53,filenames:["_modules/datapunt_processing.rst","_modules/datapunt_processing.extract.rst","_modules/datapunt_processing.helpers.rst","_modules/datapunt_processing.load.rst","_modules/datapunt_processing.transform.rst","_modules/datapunt_processing.transform.enrichment.rst","_modules/datapunt_processing.transform.geospatial.rst","_modules/datapunt_processing.transform.preprocessing.rst","_modules/modules.rst","extract/download_from_api_brk.rst","extract/download_from_api_kvk.rst","extract/download_from_api_tellus.rst","extract/download_from_api_with_authentication.rst","extract/download_from_catalog.rst","extract/download_from_objectstore.rst","extract/download_from_wfs.rst","index.rst","introduction.rst","license.rst","load/load_file_to_ckan.rst","load/load_file_to_objectstore.rst","load/load_wfs_into_postgres.rst","load/load_xls_into_postgres.rst","modules.rst","transform/enrichment/add_knmi_data.rst","transform/enrichment/add_public_events.rst","transform/geospatial/api_clean_BAG_address_NED.rst","transform/geospatial/api_get_area_codes_from_latlon.rst","transform/geospatial/api_get_nearest_address_from_coordinate.rst","transform/geospatial/divide_bbox_amsterdam_in_quadrants.rst","transform/geospatial/postgres_add_areas_from_coordinates.rst","transform/geospatial/rd_to_wgs84.rst"],objects:{"":{datapunt_processing:[0,0,0,"-"]},"datapunt_processing.boilerplate_function":{main:[0,1,1,""],parser:[0,1,1,""],your_first_function:[0,1,1,""],your_second_function:[0,1,1,""]},"datapunt_processing.extract":{csv_dataframe:[1,0,0,"-"],download_bbga_by_variable__area_year:[1,0,0,"-"],download_from_api_brk:[1,0,0,"-"],download_from_api_kvk:[1,0,0,"-"],download_from_api_tellus:[1,0,0,"-"],download_from_api_with_authentication:[1,0,0,"-"],download_from_catalog:[1,0,0,"-"],download_from_objectstore:[1,0,0,"-"],download_from_wfs:[1,0,0,"-"]},"datapunt_processing.extract.csv_dataframe":{is_valid_file:[1,1,1,""],main:[1,1,1,""],parser:[1,1,1,""],read_crow_file:[1,1,1,""],read_mora_file:[1,1,1,""],strip_cols:[1,1,1,""],valid_date:[1,1,1,""]},"datapunt_processing.extract.download_bbga_by_variable__area_year":{main:[1,1,1,""],statisticsByAreaByYear:[1,1,1,""],writeStatisticsTable2PGTable:[1,1,1,""]},"datapunt_processing.extract.download_from_api_brk":{getJsonData:[1,1,1,""],main:[1,1,1,""],parser:[1,1,1,""]},"datapunt_processing.extract.download_from_api_kvk":{get_kvk_json:[1,1,1,""],main:[1,1,1,""],parser:[1,1,1,""],response_to_json:[1,1,1,""]},"datapunt_processing.extract.download_from_api_tellus":{conversionListCvalues:[1,1,1,""],getJsonData:[1,1,1,""],get_data:[1,1,1,""],main:[1,1,1,""],parser:[1,1,1,""],reformatData:[1,1,1,""]},"datapunt_processing.extract.download_from_api_with_authentication":{getJsonData:[1,1,1,""],main:[1,1,1,""],parser:[1,1,1,""],retrywithtrailingslash:[1,1,1,""]},"datapunt_processing.extract.download_from_catalog":{download_all_files:[1,1,1,""],download_file:[1,1,1,""],download_metadata:[1,1,1,""],get_catalog_package_id:[1,1,1,""],main:[1,1,1,""],parser:[1,1,1,""]},"datapunt_processing.extract.download_from_objectstore":{download_container:[1,1,1,""],download_containers:[1,1,1,""],get_full_container_list:[1,1,1,""],main:[1,1,1,""],parser:[1,1,1,""]},"datapunt_processing.extract.download_from_wfs":{get_layer_from_wfs:[1,1,1,""],get_layers_from_wfs:[1,1,1,""],get_multiple_geojson_from_wfs:[1,1,1,""],main:[1,1,1,""],parser:[1,1,1,""]},"datapunt_processing.helpers":{connections:[2,0,0,"-"],files:[2,0,0,"-"],getaccesstoken:[2,0,0,"-"],json_dict_handlers:[2,0,0,"-"],logging:[2,0,0,"-"],xml_handlers:[2,0,0,"-"]},"datapunt_processing.helpers.connections":{execute_sql:[2,1,1,""],get_config:[2,1,1,""],objectstore_connection:[2,1,1,""],postgres_engine_pandas:[2,1,1,""],psycopg_connection_string:[2,1,1,""]},"datapunt_processing.helpers.files":{create_dir_if_not_exists:[2,1,1,""],save_file:[2,1,1,""],unzip:[2,1,1,""]},"datapunt_processing.helpers.getaccesstoken":{GetAccessToken:[2,2,1,""],parser:[2,1,1,""]},"datapunt_processing.helpers.getaccesstoken.GetAccessToken":{getAccessToken:[2,3,1,""]},"datapunt_processing.helpers.json_dict_handlers":{clean_dict:[2,1,1,""],flatten_json:[2,1,1,""],joinByKeyNames:[2,1,1,""],jsonPoints2geojson:[2,1,1,""],openJsonArrayKeyDict2FlattenedJson:[2,1,1,""]},"datapunt_processing.helpers.logging":{logger:[2,1,1,""]},"datapunt_processing.helpers.xml_handlers":{parse_and_remove:[2,1,1,""]},"datapunt_processing.load":{load_file_to_ckan:[3,0,0,"-"],load_file_to_objectstore:[3,0,0,"-"],load_wfs_to_postgres:[3,0,0,"-"],load_xls_to_postgres:[3,0,0,"-"]},"datapunt_processing.load.load_file_to_ckan":{find_resource_id_if_exists:[3,1,1,""],main:[3,1,1,""],parser:[3,1,1,""],upload_file_to_ckan:[3,1,1,""]},"datapunt_processing.load.load_file_to_objectstore":{check_existence_object:[3,1,1,""],get_object:[3,1,1,""],main:[3,1,1,""],parser:[3,1,1,""],put_object:[3,1,1,""],upload_file:[3,1,1,""]},"datapunt_processing.load.load_wfs_to_postgres":{NonZeroReturnCode:[3,4,1,""],load_layers:[3,1,1,""],main:[3,1,1,""],parser:[3,1,1,""],run_command_sync:[3,1,1,""],scrub:[3,1,1,""],wfs2psql:[3,1,1,""]},"datapunt_processing.load.load_xls_to_postgres":{load_xls:[3,1,1,""],main:[3,1,1,""],parser:[3,1,1,""]},"datapunt_processing.transform":{enrichment:[5,0,0,"-"],geospatial:[6,0,0,"-"],preprocessing:[7,0,0,"-"]},"datapunt_processing.transform.enrichment":{add_knmi_data:[24,0,0,"-"],add_public_events:[5,0,0,"-"],knmi_metadata:[5,0,0,"-"]},"datapunt_processing.transform.enrichment.add_knmi_data":{chunk_splitter:[24,1,1,""],get_day_data_dataframe:[24,1,1,""],get_day_data_raw:[24,1,1,""],main:[5,1,1,""],parse_dataframe:[5,1,1,""],parse_day_data:[24,1,1,""],parser:[24,1,1,""]},"datapunt_processing.transform.enrichment.add_public_events":{get_event_json:[5,1,1,""],main:[5,1,1,""],parser:[5,1,1,""]},"datapunt_processing.transform.enrichment.knmi_metadata":{Station:[5,2,1,""]},"datapunt_processing.transform.enrichment.knmi_metadata.Station":{altitude:[5,5,1,""],latitude:[5,5,1,""],longitude:[5,5,1,""],name:[5,5,1,""],number:[5,5,1,""]},"datapunt_processing.transform.geospatial":{addres_to_latlon_in_df:[6,0,0,"-"],api_clean_BAG_address_NED:[6,0,0,"-"],api_get_areacodes_from_latlon:[6,0,0,"-"],api_get_nearest_address_from_latlon:[6,0,0,"-"],csv_get_centroid_of_street:[6,0,0,"-"],divide_bbox_amsterdam_in_quadrants:[6,0,0,"-"],postgres_add_areas_from_coordinates:[6,0,0,"-"],rd_to_wgs84:[6,0,0,"-"]},"datapunt_processing.transform.geospatial.addres_to_latlon_in_df":{adress_to_latlon:[6,1,1,""]},"datapunt_processing.transform.geospatial.api_clean_BAG_address_NED":{main:[6,1,1,""],parser:[6,1,1,""]},"datapunt_processing.transform.geospatial.api_get_areacodes_from_latlon":{getAreaCodes:[6,1,1,""],getAreaCodesforDataFrame:[6,1,1,""],getJson:[6,1,1,""]},"datapunt_processing.transform.geospatial.api_get_nearest_address_from_latlon":{get_address_near_point:[6,1,1,""],get_openbareruimte:[6,1,1,""]},"datapunt_processing.transform.geospatial.csv_get_centroid_of_street":{get_centroid_street:[6,1,1,""],main:[6,1,1,""],parser:[6,1,1,""]},"datapunt_processing.transform.geospatial.divide_bbox_amsterdam_in_quadrants":{calculation:[6,1,1,""]},"datapunt_processing.transform.geospatial.postgres_add_areas_from_coordinates":{executeScriptsFromFile:[6,1,1,""],main:[6,1,1,""],parser:[6,1,1,""]},"datapunt_processing.transform.geospatial.rd_to_wgs84":{rd_to_wgs84:[6,1,1,""]},"datapunt_processing.transform.preprocessing":{data_selection:[7,0,0,"-"],enrichment:[7,0,0,"-"],ml_helperfunctions:[7,0,0,"-"],utilities:[7,0,0,"-"]},"datapunt_processing.transform.preprocessing.data_selection":{DateRange:[7,2,1,""],remove_nan_targets:[7,1,1,""],select_and_report:[7,1,1,""]},"datapunt_processing.transform.preprocessing.data_selection.DateRange":{from_dataframe:[7,6,1,""],length:[7,3,1,""],select:[7,3,1,""]},"datapunt_processing.transform.preprocessing.enrichment":{enrich_datetime:[7,1,1,""]},"datapunt_processing.transform.preprocessing.ml_helperfunctions":{accuracy_score:[7,1,1,""],calculate_covariance_matrix:[7,1,1,""],calculate_std_dev:[7,1,1,""],calculate_variance:[7,1,1,""],euclidean_distance:[7,1,1,""],mean_squared_error:[7,1,1,""]},"datapunt_processing.transform.preprocessing.utilities":{BigFile:[7,2,1,""],assert_unique:[7,1,1,""],calc_error:[7,1,1,""],cols_not_in:[7,1,1,""],get_last_full_year:[7,1,1,""],get_script_dir:[7,1,1,""],is_numeric:[7,1,1,""],merge_and_report:[7,1,1,""],optional_make_dir:[7,1,1,""],pickle_big_dump:[7,1,1,""],pickle_big_load:[7,1,1,""],rms:[7,1,1,""]},"datapunt_processing.transform.preprocessing.utilities.BigFile":{read:[7,3,1,""],write:[7,3,1,""]},datapunt_processing:{boilerplate_function:[0,0,0,"-"],extract:[1,0,0,"-"],helpers:[2,0,0,"-"],load:[3,0,0,"-"],transform:[4,0,0,"-"]}},objnames:{"0":["py","module","Python module"],"1":["py","function","Python function"],"2":["py","class","Python class"],"3":["py","method","Python method"],"4":["py","exception","Python exception"],"5":["py","attribute","Python attribute"],"6":["py","staticmethod","Python static method"]},objtypes:{"0":"py:module","1":"py:function","2":"py:class","3":"py:method","4":"py:exception","5":"py:attribute","6":"py:staticmethod"},terms:{"1gb":7,"292678dee13c":[1,13],"2f3":[1,13],"2faction":[1,13],"2fapi":[1,13],"2fpackage_show":[1,13],"3d5d84c216":[1,13],"3fid":[1,13],"8b69":[1,13],"boolean":7,"break":17,"byte":7,"case":[1,6,11,18,29],"class":[2,5,7],"default":[5,12,15,24],"export":[2,9,10,12,14,15,19,20,21,23,30],"final":18,"float":7,"function":[0,1,2,3,5,6,7,17,23],"import":[2,3,17,18,20],"int":[5,7,24],"new":[6,17,27],"potenti\u00ebl":[5,24],"public":[5,23,25],"return":[0,1,2,3,5,6,7,9,10,11,12,14,15,19,20,21,24,25,26,27,28,29],"static":7,"throw":7,"true":[2,3,7,21],For:[2,9,12,13,17,18,30],Such:18,The:[1,2,3,15,17,18,20],Use:[6,9,10,14,19,20,23,26,30,31],Used:[3,21],Uses:[3,20],WFS:[1,3,6,15,21,29,30],aanvalsplan_schoon:[1,3,14,20],abil:18,abl:[17,18],about:17,abov:18,absenc:18,absolut:18,acc:[1,2,9,11,12],access:2,access_token:[1,12],accesstoken:[1,2,9,11,12],account:17,accur:18,accuraci:7,accuracy_scor:7,achtergrond:[5,24],action:[1,13,18],activ:17,ad83:[1,13],add:[0,1,2,3,5,6,7,9,10,11,12,13,14,15,16,18,19,20,21,24,25,26],add_knmi_data:[0,4,16,23],add_public_ev:[0,4,16,23],added:[1,10,11],adding:2,addition:18,addr:[6,28],addres_to_latlon_in_df:[0,4],address:[6,26,27,28],adr:6,adress:6,adress_to_latlon:6,affect:18,affero:18,after:18,afvalcontain:[3,19],afvaldata:1,against:18,agre:18,agreement:18,alia:5,all:[1,2,5,7,11,13,14,15,17,18,24,30],alleg:18,allow:18,allow_fail:[3,21],almost:7,alon:[17,18],also:[7,17,18],alter:18,altitud:5,amsterdam:[1,2,3,5,6,9,11,12,13,15,17,19,21,23,24,25,26,27,29],amsterdam_hotspot:26,an_example_pypi_project:[0,2,3,6,19,26],anaconda:17,analist:17,analyt:17,ani:18,another_fold:[1,15],anotherdir:2,anyon:18,api:[1,2,3,6,9,10,11,12,13,17,19,21,23,26,27],api_clean_bag_address_n:[0,4,16,23],api_get_areacodes_from_latlon:[0,4,16,23],api_get_nearest_address_from_latlon:[0,4,16,23],api_kei:[1,3,10,19],app:[1,3,13,14,20],apparatu:18,appli:[7,17,18],applic:[3,20],appropri:2,area:[1,6,27,30],areatyp:1,arg:[0,1,2,3,5,6,7,9,10,11,12,13,14,15,19,20,21,24,25,27,28,29],argname1:0,argname2:0,argpars:17,argument:[0,1,2,3,5,6,17,25],arrai:[2,7],assert:[7,18],assert_uniqu:7,assum:18,attach:18,attempt:18,attr2:2,attr:2,auth:[1,9,11,12,21,22],authent:[2,12,30],author:[9,11,18],authorization_level:[2,9,12],authurl:2,automat:[17,18],autorisati:12,avail:[2,18,24],awesom:17,awesome_modul:17,b826:[1,13],back:18,bag:[6,27],bar:2,base:[2,3,5,6,7,20,27,28],base_url:10,bash:17,basi:18,basic:[2,16],batch:7,bbga:1,bbox:[6,29],becom:18,been:18,befor:[10,14,20],begin:[5,24],behalf:18,behorend:6,beleid:12,believ:18,below:17,benefici:18,better:[6,31],between:7,bewolk:[5,24],bi_afv:1,big:7,bigfil:7,bij:6,bin:17,blob:[2,9,12],block:17,boilerplate_funct:[8,17],bool:[5,7,24],both:7,branchnumb:[1,10],bring:18,brk:[1,2,9,12],brought:18,buffer:7,build:17,busi:18,buurt:[1,6,15,27],buurtcombinati:[1,6,15,27],buurten:[],bytearrai:7,c1f04a62:[1,13],c60:[1,11],calc_error:7,calcul:[6,7,29],calculate_covariance_matrix:7,calculate_std_dev:7,calculate_vari:7,call:[10,17],can:[1,3,5,7,9,12,17,18,19,24],catalog:[1,3,13,19,23],catalogu:[1,3,13,19],categori:24,caus:18,ce2647a076ef:[1,13],centroid:6,chang:[1,17],charact:18,charg:18,check:[0,2,3,20],check_existence_object:[3,20],choic:[12,15,18],choos:[9,12,15,18],chunk:[5,24],chunk_splitt:[5,24],circumst:18,citi:[1,6,10,17,26,29],citizen:1,city_nam:6,ckan:[1,3,13,19,23],ckan_api_kei:19,clean:[1,26],clean_dict:2,clear:18,clone:17,cloud:17,cmd:[3,21],code:[2,3,6,16,20,21,27,30],coenhaven:24,cols_not_in:7,column:[1,2,6,7,27],com:[2,3,9,12,17,20],combin:[17,18],come:18,comma:[1,2,14,15],command:[1,3,5,9,10,11,12,13,14,15,17,19,20,21,24,25,26,30],commandlin:[0,1,2,3,6,9,10,11,12,13,14,17,19,20,21,26],commerci:18,common:[18,23],commonli:23,compani:10,compar:7,complet:18,complianc:18,compliant:18,compos:17,comput:18,concern:18,concole_script:[],conenct:1,config:[2,14,17,20,21,22,23,30],config_full_path:2,config_nam:[2,14,20],config_path:[3,14,20,21,22],configur:2,conflict:18,conn:2,connect:[0,1,3,8,14,17,20,21],consequenti:18,consist:[1,11],consol:[2,3,21],console_script:17,constitut:18,constru:18,contain:[1,2,3,7,11,14,18,20,23],container_path:[3,20],content:[8,18,20],content_typ:[3,20],contract:18,contribut:16,control:[17,18],convei:18,convers:[1,11],conversionlistcvalu:[1,11],convert:[1,2,11,17],cookbook:2,coordin:[1,6,15,28],copi:[17,18],copyright:18,core:7,correct:[6,17,18],cost:18,count:[1,11],counter:18,court:18,covari:7,creat:[1,2,3,7,11,13,17,18,20],create_dir_if_not_exist:2,creation:18,credenti:[1,2,3,9,12,17,21,23],cross:18,crow:[1,3,14,20],csv:[2,3,5,6,11,19,20,24,26],csv_datafram:[0,8],csv_get_centroid_of_street:[0,4],current:[2,5,6,9,11,12,24,27],cursor:2,cvalu:[1,11],d_bbga_cd:1,dabeaz:2,dai:[7,18],daili:[5,24],dam:6,damag:18,dashboard:17,data:[1,2,3,5,6,7,9,11,12,13,14,15,16,19,20,21,22,23,24,25,27],data_output:2,data_select:[0,4],databas:[1,17],datacentrum:[5,24],datadir:[3,22],datafram:[1,5,7,24,25],datapunt:[1,9,11,12,17],datapunt_email:[2,9,12],datapunt_password:[2,9,12],datapunt_process:[8,9,10,11,12,13,14,15,16,17,19,20,21,22,23,24,25,26,27,28,29,30,31],dataservic:[3,20],dataset:[1,2,3,7,13,19,23],dataset_nam:[3,19],datastor:[3,19],date:[1,2,5,7,24],datecol:1,daterang:7,datetim:[5,7,24],datum:1,dayofyear:7,db_config:21,db_config_nam:[2,3,22,30],dbconfig:22,dbname:[2,3,21],ddvec:[5,24],deal:[17,18],death:18,declaratori:18,defect:18,defend:18,defin:[1,3,10,12,14,15,18,20],delet:18,delta:7,depart:1,deploi:17,describ:[6,18,27],descript:[0,1,2,3,5,6,7,9,10,11,12,13,14,15,17,18,19,20,21,24,25,26],desir:[1,13,18],detail:18,dev:[2,17,21,22,30],develop:17,developp:17,deviat:7,df_std:1,dict:[1,2,10,11,17],dictionairi:[1,11],dictionari:[1,2,6,11,28],dictonari:[1,13],dienstverlen:12,differ:[6,17,18,31],dir:[1,2,9,11,12,13],direct:18,directli:[17,18],directori:[2,7,13,18,22],disclaim:[5,24],displai:18,distanc:7,distinguish:18,distributor:18,divid:[6,29],divide_bbox_amsterdam_in_quadr:[0,4,16,23],doc:[0,1,2,3,6,9,10,11,12,14,17,19,20,26],docker:[1,2,3,14,17,20,21,22,30],doctrin:18,document:[17,18],doe:[0,1,2,6,7,13,18,30,31],done:7,download:[1,3,6,9,11,12,13,14,20,31],download_all_fil:[1,13],download_bbga_by_variable__area_year:[0,8],download_contain:[1,14],download_directori:[1,13],download_fil:1,download_from_api_brk:[0,8,12,16,23],download_from_api_kvk:[0,8,16,23],download_from_api_tellu:[0,8,16,23],download_from_api_with_authent:[0,8,16,23],download_from_catalog:[0,8,16,17,23],download_from_data_amsterdam:17,download_from_data_amsterdam_api:[],download_from_data_amsterdam_catalog:13,download_from_objectstor:[0,8,16,23],download_from_wf:[0,8,16,23],download_metadata:[1,13],drafter:18,drop:7,druk:[5,24],dte:[1,13],dtf:13,dummi:30,each:[1,3,6,11,14,18,21,27],earlier:18,edit:17,een:[5,24],either:18,els:[1,15],email:[2,12],employe:[1,2,11,12],employee_plu:[1,2,9,12],empti:[1,5,7,15,24],end:[5,7,17,18,24],endpoint:[1,9,10,11,12],enforc:18,engin:2,enrich:[0,4,16,24,25],enrich_datetim:7,entir:[2,18],entiti:18,env:[1,9,10,12,19,20,21,23,30],environ:[2,10,14,17,20,21],epsg:[1,3,15,21],equival:18,error:[1,2,3,6,7,9,10,11,12,20,21,27],essenti:18,etc:[1,2,6,7,13,28],etl:[],euclidean_dist:7,ev24:[5,24],even:18,event:[5,18,25],everi:18,exampl:[0,1,2,3,6,9,10,11,12,13,14,15,17,19,20,21,22,24,25,26,30,31],except:[3,18,21],exclud:[1,15,18],exclus:18,excut:[3,21],execut:2,execute_sql:2,executescriptsfromfil:[6,30],exercis:18,exist:[1,2,3,7,13,17,20],explan:[5,24],explicitli:18,exploit:18,express:18,extens:17,extent:18,extract:[0,8,9,10,11,12,13,14,15,16,17],f5343c794b10:2,factual:18,fail:18,failur:18,fals:[2,3,5,21,24],featur:[2,7],fee:18,fetch:[5,24],fhx:[5,24],field:[2,5,17],fifti:18,file:[0,1,3,5,6,7,8,13,14,15,17,18,19,20,21,22,23,24],file_loc:1,file_nam:3,file_path:[3,7,19],filenam:[2,3,6,9,11,12,19,20,26,30],filename_as_fold:2,filename_path:[3,20],fill:[1,12,13,23],find:[2,3,7,20],find_resource_id_if_exist:3,first:[1,6,11,18,28],fit:18,flatten:[1,2,11],flatten_json:2,flattend:[1,11],folder:[1,2,13,14,15,17],follow:[12,17,18,24],foo:2,fork:17,form:[12,17],format:[1,3,5,15,21,24],forum:[6,31],found:[1,3,6,7,9,12,17,19,20,28],foundat:18,fraction:7,frame:[1,5,7,25],framework:[21,30],free:18,from:[0,1,2,3,5,6,7,9,10,11,12,13,14,15,17,18,19,20,21,23,24,25,26,27,31],from_datafram:7,full:[1,2,3,5,7,9,10,11,12,13,14,15,20,24,30],full_config_path:30,full_path:2,further:18,gdal:[21,30],gebieden:[1,6,15,21,27],gebiedsberichtwerken:1,gebiedsgerichtwerken:[1,15],gener:[1,5,7,9,11,12,14,17,18,23,24],geo:[6,29],geocach:[6,31],geojson:[1,2,15,19],geosearch:[6,27],geospati:[0,4,16,26,27,28,29,30,31],get:[1,2,5,6,9,10,11,12,13,14,15,16,24,27,28],get_address_near_point:[6,28],get_catalog_package_id:[1,13],get_centroid_street:6,get_config:2,get_data:[1,11],get_day_data_datafram:[5,24],get_day_data_raw:[5,24],get_event_json:[5,25],get_full_container_list:[1,14],get_kvk_json:[1,10],get_last_full_year:7,get_layer_from_wf:[1,15],get_layers_from_wf:[1,15],get_multiple_geojson_from_wf:[1,15],get_object:[3,20],get_openbareruimt:[6,28],get_script_dir:7,getaccesstoken:[0,1,8,9,11,12],getareacod:[6,27],getareacodesfordatafram:[6,27],getjson:[6,27],getjsondata:[1,9,11,12],gettoken:[],gis:2,git:17,github:[2,9,12,17,23],gitignor:23,give:[6,27],given:[2,12,18],global:[5,24],gml:[1,15],gnu:18,goodwil:18,govern:18,great:0,guid:17,guidelin:17,handelsregist:10,has:[7,18],have:[7,18],header:2,held:18,helper:[0,1,3,8,9,11,12,14,16,17,20],here:[1,9,12],herebi:18,hereof:18,hide:[3,21],high:17,histor:7,host:[2,3,17,21],hour:[1,11],housenumb:[1,6,10,28],how:[3,7,16,18,20],howev:18,html:[0,2,3,6,19,26],http:[0,1,2,3,5,6,9,10,11,12,13,15,17,18,19,20,24,26,27,31],huisnr:6,huisnumm:[6,28],ideal:[1,11],ignor:[7,23],imag:17,impli:18,imposs:18,inaccuraci:18,incident:18,incl:[1,14],includ:[1,2,3,5,13,15,17,18,19,20,24,30],increment:2,incremental_parsing_of_huge_xml_fil:2,incur:18,indemn:18,indemnifi:18,index:[6,16,31],indirect:18,indirectli:18,individu:18,inform:[6,17,18,27],informat:1,infring:18,ini:[2,14,17,20,21,22,23,30],initi:[2,18],injuri:18,input:[6,7,17],inseason:[5,24],insert:[2,13],instal:17,instanc:17,instead:2,intellectu:18,intend:18,intern:[2,12],intranet:12,iopub_data_rate_limit:17,is_numer:7,is_valid_fil:1,issu:17,item:[1,2,6,11,27],its:18,join:30,joinbykeynam:2,json:[1,2,3,5,6,9,10,11,12,13,15,20,25,27],json_dict_handl:[0,8],json_object:2,jsonpoints2geojson:2,judgment:18,judici:18,jupyt:17,jurisdict:18,kadast:12,kei:[2,3,19],kenni:[5,12,24],key1:2,key2:2,key_nam:2,kind:18,knmi:[5,24],knmi_metadata:[0,4],known:18,kvk:[1,10],kvk_api_kei:[1,10],kvknumber:[1,10],kwarg:[1,3,14,21],label:[1,11],languag:18,larger:7,last:7,lat:[2,6,27,28,30],latcolumn:2,later:[17,18],latitud:5,lattitud:6,law:18,layer:[1,3,15,21],layer_nam:[1,3,15,21],learn:17,least:1,leav:[1,15],left:7,legal:18,legend:[5,24],length:[1,7,11],lesser:18,lhs:7,liabl:18,librari:[21,30],licens:16,like:[6,17,18,27],limit:[1,6,11,29],line:[1,3,5,9,11,12,13,15,17,19,21,24,25,26,30],list:[1,2,3,5,6,7,10,11,13,15,17,21,24,29],load:[0,8,16,17,19,20,21,22,30],load_file_to_ckan:[0,8,16,23],load_file_to_objectstor:[0,8,16,23],load_lay:[3,21],load_wfs_to_postgr:[0,8,16,23],load_xl:[3,22],load_xls_to_postgr:[0,8,16,23],local:[1,13,14,17,21,22],locat:[1,2,3,6,9,11,12,14,15,17,18,19,22,28],log:[0,7,8],logger:2,login:[1,2,3,12,17,21],logo:18,lon:[2,6,27,28,30],loncolumn:2,longitud:5,longtitud:6,look:18,loop:[1,14],loss:18,lost:18,luchtvochtigheid:[5,24],machin:17,made:18,mai:18,main:[0,1,3,5,6,11,13,17,23],maintain:18,make:[1,17,18],malfunct:18,manag:18,mani:[7,17],manner:18,map:[1,15,17],mark:18,master:[2,9,12],match:[2,7],materi:18,matrix:[1,7,11],matter:18,max:[6,7,31],max_drop_r:7,maximum:18,mean:[7,18],mean_squared_error:7,merchant:18,merg:7,merge_and_report:7,messag:[1,2,3,6,7,9,10,11,12,21,27],met:6,metadata:[1,11,13],method:[6,18,31],mime:[3,20],miss:17,ml_helperfunct:[0,4],ml_preprocess:[0,4],mode:17,modul:[8,16,17],month:[5,24],mora:[1,14],more:[17,18],moreov:18,most:[6,23,29],mpb:13,mpl:18,mpv:13,mpz:13,mstr:[5,24],much:17,multipl:[1,2,3,6,9,11,12,14,15,22,29],must:18,my_project_fold:[9,11,12],n_unmatched_limit:7,naam:6,name:[1,2,3,5,6,9,11,12,14,15,17,18,19,20,21,22,27,28,30],nan:7,nationwid:10,nearest:[6,27,28],necessari:18,need:[13,17],neerslag:[5,24],neglig:18,nest:2,network:12,nln:[3,21],non:18,none:[1,2,3,5,7,10,20,24,25],nonzeroreturncod:[3,21],normal:[],note:[17,18],notebook:16,notebookapp:17,noth:18,notifi:18,notwithstand:18,now:[2,7],number:[1,2,5,6,7,11,13,15,18,24,29],number_of_box:[6,29],numer:7,oauth2:[9,11],obj:7,object:[1,2,3,5,6,7,9,12,14,20,24,28],objectsctor:2,objectstor:[1,2,3,14,20,23],objectstore_connect:[1,2,3,14,17,20],objectstore_password:[14,20],oblig:18,observ:24,obtain:18,offer:18,offset:[6,31],often:17,ogr2ogr:[3,21,30],one:[1,11,18],ongo:18,onli:[7,12,17,18,24],open:[2,3,20],openbar:[6,28],openbareruimt:[6,28],openjsonarraykeydict2flattenedjson:2,oper:[7,23],ophalen:[5,24],option:[0,1,2,3,5,6,7,18,19,21,24,26],optional_make_dir:7,order:18,ordinari:18,org:[0,2,3,6,18,19,26],origin:18,origion:6,osx:17,other:[1,11,17,18],otherwis:18,our:[10,17,23],output:[1,6,13,15,17],output_fold:[1,2,3,9,11,12,13,14,15,20],outputfil:11,outputfold:[9,11,12],outputformat:[1,15],outstand:18,overwrit:[3,21],own:[1,17,18],owner:[1,13],ownership:18,packag:[8,13,16,17,20,23],package_show:[1,13],page:[1,3,11,13,16,17,19],panda:[2,5,6,7,22,24,27],param:[1,7,10],paramet:[1,2,7,10,17],pars:[1,2,5,6,9,10,11,12,24,25,27],parse_and_remov:2,parse_datafram:5,parse_day_data:[5,24],parser:[0,1,2,3,5,6,9,10,11,12,13,14,15,19,20,21,24,25,26],part:[5,18,24],parti:18,particular:18,password:[2,3,12,14,20,21,23],path:[0,1,2,3,7,10,13,14,15,19,20,21,30],path_to_config:[2,14,20],path_to_fold:[1,15],pdok:26,percent:18,perform:[7,18],permit:18,person:18,pg_str:[2,3,6,21,30],pgn:[5,24],pgx:[5,24],php:[6,31],pickl:7,pickle_big_dump:7,pickle_big_load:7,piec:[5,24],pip:17,pipelin:17,place:18,pleas:17,point:[2,17],popul:7,port:[2,3,17,21],portion:18,posit:[],possibl:[0,2,3,6,12,15,18,19,26],postalcod:[1,10],postcod:[6,28],postgr:[2,3,6,17,21,22,30,31],postgres_add_areas_from_coordin:[0,4,16,23],postgres_engine_panda:2,postgresql:[3,21,22,23],power:18,prcp:[5,24],pre:[5,24],predict:7,prefer:18,prefix:[1,3,14,20],preprocess:[0,4,17],prequisit:16,present:[3,7,20],prevent:[18,23],princip:18,print:[1,2,15],print_config_var:2,prior:18,prioriti:7,privat:[3,19],process:[18,23],profil:[3,19],profit:18,program:[3,21,30],programma:12,prohibit:18,project:[17,23],projectdir:[15,22],prompt:17,proper:[1,11,17,21,23],properti:18,prove:18,provid:[1,2,10,18],provis:18,provision:18,psycopg2:[2,3,21],psycopg:2,psycopg_connection_str:2,publish:18,purpos:18,put:[13,18],put_object:[3,20],pypi:17,python3:17,python:[2,3,17,20,24],pythonhost:[0,2,3,6,19,26],quadrant:[6,29],qualiti:[17,18],queri:[2,6,29],question:[2,3,20],quick:[6,31],quot:2,radiu:[6,27,28],rais:7,rang:7,raw:[5,23,24],rd_to_wgs84:[0,4,16,23],read:[2,5,7,17,24],read_crow_fil:1,read_mora_fil:1,reason:[18,24],receipt:18,receiv:18,reciev:12,recipi:18,record:[1,11],rectangl:[6,29],refer:18,reform:18,reformat:[1,11],reformatdata:[1,11],refresh:[1,13],regener:17,regist:12,registr:[1,11],reinstat:18,rel:21,relat:18,relev:[5,18,24],remedi:18,remov:[2,7,18],remove_nan_target:7,renam:18,repair:18,report:7,repositori:17,repres:[7,18],reproduc:[17,18],reproject:[6,31],request:2,requir:[2,12,17,18],resel:18,resid:[6,28],resourc:[1,13],respect:18,respons:[1,5,9,10,11,12,13,24],response_to_json:1,restrict:18,result:[1,3,6,13,14,18,20,27,28,31],retriev:[1,11,13],retrievd:[3,20],retrywithtrailingslash:1,reus:17,rhs:7,right:[7,18],risk:18,rms:7,root:[1,2,7,14],row:[1,6,7,11,27],royalti:18,rsin:[1,10],rsn:[1,2,9,12],rst:17,ruimt:[6,28],run:[0,1,2,3,5,6,7,9,10,11,12,13,14,15,17,19,20,21,24,25,26],run_command_sync:[3,21],runnabl:17,sale:18,save:[1,2,3,9,11,12,15,20],save_fil:2,schedul:7,schema:1,schiphol:24,scope:[1,2,9,11,12],script:[2,5,10,12,14,17,20,24],scrub:[3,21],search:[6,10,27],searchabl:[],section:18,see:[0,2,3,5,6,7,17,18,19,24,26],select:7,select_and_report:7,sell:18,semant:17,send:12,separ:[1,2,5,14,15,18,22,24],seri:7,server:17,servic:[1,3,9,11,15,18,21],session:[1,2,14],set:[1,2,11,15,17,21,22],setup:[1,2,14,17],setuptool:17,shall:18,shapezip:[1,15],share:18,shell:17,should:18,show:0,showtop:[6,31],side:[7,17],simpl:1,simplic:24,singl:[1,15],skill:18,skip:17,some:[0,17,18],sourc:[2,17],space:[1,15],spatial:23,special:18,specif:[6,18,27],specifi:[1,2,3,5,10,13,14,15,20,24],speed:[1,11],sphinx:[0,1,2,3,5,6,9,10,11,12,13,14,15,17,19,20,21,24,25,26],sql:2,sqlalchemi:2,squar:7,src:2,srs:[1,15],st_transform:[6,31],stackexchang:2,stackoverflow:[3,20],stadsdeel:[1,6,15,27],stand:17,standard:[1,7,15],start:[5,7,16,24],stat:7,station:[5,24],statisticsbyareabyyear:1,statutori:18,step:16,steward:18,stoppag:18,store:[0,1,3,13,14,19,20,23],str:[3,5,7,20,24],straat:6,strale:[5,24],street:[1,6,10,28],street_column:6,string:[2,3,5,6,21,24],strip_col:1,structur:17,stuff:0,style:[0,2,3,6,19,26],sub:[1,14],subfold:[1,2,3,14,20],subject:18,subkei:2,sublicens:18,submodul:[4,8],subpackag:8,subprocess:[3,21],substanc:18,subsubfold:[1,14],subsubkei:2,successfulli:[3,20],suffici:18,suffix:2,suitabl:17,sunr:[5,24],support:[7,18],sure:1,surviv:18,system:[1,15,17],t10n:[5,24],t_sr:[3,21],tabl:[1,2,22,30],tablenam:1,tag:[1,14],target:[1,7],tellu:[1,11,12],tellus_metadata:[1,11],tellusdata:[11,12],temp:[5,24],temperatuur:[5,24],tenminst:6,termin:17,test:[1,3,11,13,17,20,26],testdata:26,testus:23,text:[2,3,18,20],than:[7,18],thei:18,them:[1,2,15,17,23],theori:18,thereof:18,thi:[1,2,6,7,10,11,12,13,14,17,18,20,23,30],third:18,those:[17,18],through:[1,14],time:[1,7,18],timedelta:7,titl:[1,3,15,21],tll:[1,2,9,11,12],to_sql:[2,22],todai:[5,24],todo:2,toegevoegd:6,token:[1,2,9,11,12],top:2,topografi:13,tort:18,total:1,towardsdatasci:2,trademark:18,tradenam:[1,10],transfer:18,transform:[0,8,16,17,24,25,26,27,28,29,30,31],tripl:2,truth:7,tupl:5,two:[6,7,27],txt:[0,1,2,3,15,20],type:[1,2,3,7,11,12,17,20,21],under:18,understand:18,unenforc:18,uniqu:[1,7,13],unless:18,unmodifi:18,unstruct:17,until:18,unzip:[1,2,13],upload:[3,19,20,21,22,23],upload_fil:[3,20],upload_file_to_ckan:[3,19],url:[1,2,3,6,9,10,11,12,13,15,19,21,27],url_api:[1,11],url_wf:[1,15],usag:[2,9,10,11,12,13,14,15,16,17,19,20,21,22,24,25,26,30],use:[2,3,6,16,18,20,21,23,29],used:[7,17,18,23],user:[2,3,12,18,19,21],usertyp:[1,2,9,11,12],uses:[2,12],using:[1,2,3,9,11,12,14,17,18,20,21,22,30],util:[0,1,4],valid_d:1,validli:18,valu:[1,2,6,7,10,11,27],van:6,vanuit:[5,24],variabelen:[1,6],variabl:[1,2,5,10,12,19,23,24],variablenam:1,varianc:7,vector:7,venv:17,verblijfsobject:[6,27],verdamp:[5,24],version:17,via:[],vicl:[5,24],viewabl:12,virtual:[17,21,30],virtualenv:17,volgend:6,vvn:[5,24],vvx:[5,24],waaraan:6,want:[1,6,9,11,12,17,18,24,31],weather:[5,24],week:7,well:[6,29],were:7,wfs2psql:[3,21],wfs:[1,15],wfs_get_geojson:15,what:7,when:[3,7,12,17,20],where:[1,2,6,13,14,18,20,23,28],whether:18,which:[1,3,6,7,11,12,17,18,19,27],who:18,wide:18,wind:[5,24],window:17,wip:[6,30],within:[3,18,21],without:[1,2,15,18],work:[2,6,27,29,30],workflow:17,world:18,would:18,wrapper:[2,7,24],write:[1,3,7,14,20,30],writestatisticstable2pgt:1,written:[1,14],www:[5,24],xls:[1,22],xlsx:[1,3,22],xml:2,xml_handler:[0,8],y_pred:7,y_true:7,year:[1,7],yet:[1,2,6,7,13,30],yield:[5,24],yml:17,you:[1,6,7,9,10,11,12,17,24,31],your:[1,2,3,10,14,17,19,20],your_file_nam:[0,3,20],your_first_funct:0,your_second_funct:0,zeeniveau:[5,24],zicht:[5,24],zijn:6,zip:2,zipfil:2,zonneschijnduur:[5,24],zsh:17},titles:["datapunt_processing package","datapunt_processing.extract package","datapunt_processing.helpers package","datapunt_processing.load package","datapunt_processing.transform package","datapunt_processing.transform.enrichment package","datapunt_processing.transform.geospatial package","datapunt_processing.transform.preprocessing package","src","download_from_api_brk","download_from_api_kvk","download_from_api_tellus","download_from_api_with_authentication","download_from_catalog","download_from_objectstore","download_from_wfs","Datapunt Processing","Data-processing","Mozilla Public License Version 2.0","load_file_to_ckan","load_file_to_objectstore","load_wfs_to_postgres","load_xls_to_postgres","Modules","add_knmi_data","add_public_events","api_clean_BAG_address_NED","api_get_areacodes_from_latlon","api_get_nearest_address_from_latlon","divide_bbox_amsterdam_in_quadrants","postgres_add_areas_from_coordinates","rd_to_wgs84"],titleterms:{"function":[9,10,11,12,13,14,15,16,19,20,21,22,24,25,26,27,28,29,30,31],"new":18,"public":18,Use:18,With:18,add:17,add_knmi_data:[5,24],add_public_ev:[5,25],addit:18,addres_to_latlon_in_df:6,api_clean_bag_address_n:[6,26],api_get_areacodes_from_latlon:[6,27],api_get_nearest_address_from_latlon:[6,28],api_get_nearest_address_from_point:[],applic:18,argument:[9,10,11,12,13,14,15,19,20,21,22,24,26,30],authent:[],basic:23,boilerplate_funct:0,claim:18,code:[17,18],compli:18,condit:18,config:[],connect:2,content:[0,1,2,3,4,5,6,7],contribut:[17,18],contributor:18,cover:18,csv_datafram:1,csv_get_centroid_of_street:6,data:17,data_select:7,datapunt:16,datapunt_process:[0,1,2,3,4,5,6,7],date:18,definit:18,disclaim:18,distribut:18,divide_bbox_amsterdam_in_quadr:[6,29],download_bbga_by_variable__area_year:1,download_from_api_brk:[1,9],download_from_api_kvk:[1,10],download_from_api_tellu:[1,11],download_from_api_with_authent:[1,12],download_from_catalog:[1,13],download_from_data_amsterdam_api:[],download_from_data_amsterdam_catalog:[],download_from_objectstor:[1,14],download_from_wf:[1,15],due:18,effect:18,enrich:[5,7,23],execut:18,exhibit:18,extract:[1,23],fair:18,file:2,form:18,geospati:[6,23],get:17,getaccesstoken:2,grant:18,helper:[2,23],how:17,inabl:18,incompat:18,json_dict_handl:2,knmi_metadata:5,larger:18,liabil:18,licens:18,limit:18,litig:18,load:[3,23],load_file_to_ckan:[3,19],load_file_to_objectstor:[3,20],load_wfs_to_postgr:[3,21],load_xls_to_postgr:[3,22],log:2,miscellan:18,ml_helperfunct:7,ml_preprocess:7,modif:18,modifi:18,modul:[0,1,2,3,4,5,6,7,23],mozilla:18,name:26,normal:[],notebook:17,notic:18,packag:[0,1,2,3,4,5,6,7],patent:18,posit:[9,10,11,12,13,14,15,19,20,21,22,24,26,30],postgres_add_areas_from_coordin:[6,30],preprocess:7,prequisit:17,process:[16,17],rd_to_wgs84:[6,31],regul:18,represent:18,respons:18,scope:18,search:16,secondari:18,softwar:18,sourc:18,src:8,start:17,statut:18,step:17,submodul:[0,1,2,3,5,6,7],subpackag:[0,4],subsequ:18,term:18,termin:18,transform:[4,5,6,7,23],usag:23,use:17,util:7,version:18,warranti:18,work:18,xml_handler:2,you:18,your:18}})