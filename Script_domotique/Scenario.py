#o!/usr/bin/python

# -*- coding: utf-8 -*-


import serial
import MySQLdb
import datetime
import time
import urllib
import urllib2
import sys
import os
import msql
import json



processus = 'mysqld'

s = os.popen('ps ax').read()

while processus not in s:

	n = 1

	time.sleep(0.2)

	s = os.popen('ps ax').read()



try:

	db = MySQLdb.connect(msql.host, msql.usr, msql.pwd, msql.db)

	time.sleep(0.2)

	cursor = db.cursor()



except db.Error, e:

	urllib.urlopen("http://notify8702.freeheberg.org/?id=thibault&notif=Erreur connection bdd Scenario&id_notif:-8")

	print time.strftime('%A %d. %B %Y  %H:%M',time.localtime()) + " Error Scenario %d: %s" % (e.args[0],e.args[1])

	sys.exit(1)





ser = serial.Serial( port = '/dev/ttyACM0', baudrate =9600 )

	

while True:	

	try:

		time.sleep(0.2)

		#sql_Liste_Scenario = "SELECT XmlID,count(*) as NbScenario from Scenario Group by XmlID"

		sql_Liste_Scenario = "SELECT XmlID,Conditions,Actions, SequenceNo,Scenario_Xml.Name, Scenario_Xml.status FROM Scenario  inner join Scenario_Xml on Scenario_Xml.ID = Scenario.XmlID where status = 1 ORDER BY XmlID, SequenceNo"

		#print (sql_Liste_Scenario)

		cursor.execute(sql_Liste_Scenario)

		Old_XmlID = -5555

		#############   LISTE LES SCENARIO   ##############

		for row in cursor.fetchall():			

			XmlID = int(row[0])

			Conditions = row[1]

			Actions = row[2]

			SequenceNo = row[3]			

			ScenarioName = row[4]		

			Status = row[5]

			#print row

			#print "////////////////"

			if Status == 1:

				Conditions_SQL =""

				conditions_Where =""

				Conditions = Conditions.replace("(","").replace(")","")

				max_row_id =0;	

				if len(Conditions.split(" and ")) > 1:

					NbAnd = Conditions.count(" and ")

					Len_And =  range(len(Conditions.split(" and ")))

					##if NbAnd > 0:

						##Conditions=Conditions.replace("and","or")

					Conditions_And = Conditions.split("and")				

					for row_Len_And in Len_And:
						row_id = str(row_Len_And)
						max_row_id = int(row_id)
						Conditions_SQL += "inner join cmd_device as e"+row_id+" on "
						Conditions_SQL += Conditions_And[row_Len_And].replace("timeofday  ==","(HOUR(now())*60+MINUTE(now())) =").replace("timeofday ","(HOUR(now())*60+MINUTE(now())) ").replace("timeofsun  ==","(select DATE_FORMAT(now(), '%H:%i')) = ").replace("weekday  ==","WEEKDAY(now()) =").replace("==","and e"+row_id+".Etat=",).replace("device[","e"+row_id+".id=").replace("]","").replace("On",'1').replace("Off",'0').replace("@Sunrise","( select DATE_FORMAT(str_to_date(Value, '%H:%i'),'%H:%i') from cmd_device where cmd_device.Nom = 'Sunrise')").replace("@Sunset","( select DATE_FORMAT(str_to_date(Value, '%H:%i'),'%H:%i') from cmd_device where cmd_device.Nom = 'Sunset')")

					#Conditions_SQL = "where "
					#Conditions_SQL += Conditions.replace("timeofday  ==","(HOUR(now())*60+MINUTE(now())) =").replace("timeofday ","(HOUR(now())*60+MINUTE(now())) ").replace("timeofsun  ==","(select DATE_FORMAT(now(), '%H:%i')) = ").replace("weekday  ==","WEEKDAY(now()) =").replace("==","and Etat_IO.Etat=",).replace("device[","Etat_IO.id=").replace("]","").replace("On",'1').replace("Off",'0').replace("@Sunrise","(select DATE_FORMAT(sunrise, '%H:%i') from Sunrise_set)").replace("@Sunset","(select DATE_FORMAT(sunset, '%H:%i') from Sunrise_set)")
					#print Conditions_SQL
				

				if len(Conditions.split(" or ")) > 1:

					Len_OR =  range(len(Conditions.split(" or ")))

					Conditions_OR = Conditions.split(" or ")

					max_row_id = max_row_id+1

					for row_Len_OR in Len_OR:

						row_id = str(int(row_Len_OR)+int(max_row_id))

						Conditions_SQL += "left join cmd_device as e"+row_id+" on "

						Conditions_SQL += Conditions_OR[row_Len_OR].replace("timeofday  ==","(HOUR(now())*60+MINUTE(now())) =").replace("timeofday ","(HOUR(now())*60+MINUTE(now()))").replace("timeofsun  ==","(select DATE_FORMAT(now(), '%H:%i')) = ").replace("weekday  ==","WEEKDAY(now()) =").replace("==","and e"+row_id+".Etat=",).replace(">=","and Etat >=",).replace("<=","and Etat <=",).replace(">","and Etat >",).replace("<","and Etat <",).replace("device[","e"+row_id+".id=").replace("]","").replace("On",'1').replace("Off",'0').replace("@Sunrise","( select DATE_FORMAT(str_to_date(Value, '%H:%i'),'%H:%i') from cmd_device where cmd_device.Nom = 'Sunrise')").replace("@Sunset","( select DATE_FORMAT(str_to_date(Value, '%H:%i'),'%H:%i') from cmd_device where cmd_device.Nom = 'Sunset')")

						if conditions_Where !="":

							conditions_Where += " or "

						conditions_Where +=  " e"+row_id+".ID is not null"



				if Conditions_SQL == "":

					Conditions_SQL+= " " 

					conditions_Where += Conditions.replace("timeofday  ==","(HOUR(now())*60+MINUTE(now())) =").replace("timeofsun  ==","(select DATE_FORMAT(now(), '%H:%i')) = ").replace("weekday  ==","WEEKDAY(now()) =").replace("==","and Etat=",).replace(">=","and Etat >=",).replace("<=","and Etat <=",).replace(">","and Etat >",).replace("<","and Etat <",).replace("device[","id=").replace("]","").replace("On",'1').replace("Off",'0').replace("@Sunrise","( select DATE_FORMAT(str_to_date(Value, '%H:%i'),'%H:%i') from cmd_device where cmd_device.Nom = 'Sunrise')").replace("@Sunset","( select DATE_FORMAT(str_to_date(Value, '%H:%i'),'%H:%i') from cmd_device where cmd_device.Nom = 'Sunset')")

				

				if conditions_Where !="":

					conditions_Where= "where "+conditions_Where



				Actions = Actions.split(",")

				#print Conditions_SQL

				#print conditions_Where

				############ SI NOUVEAU SCENARIO   #################
				
				if XmlID != Old_XmlID:
					#Old_XmlID = XmlID

					#sql_check_etat =  "SELECT CASE WHEN EXISTS ( select * from Etat_IO where "+Conditions+") then 1 else 0 end ;"

					#sql_check_etat =  "SELECT COUNT(*) as result from Etat_IO where "+Conditions+" ;"		

					if Conditions_SQL != "" or conditions_Where != "":

						sql_check_etat =  "SELECT COUNT(*) as result from cmd_device "+Conditions_SQL+" "+conditions_Where+" ;"

						cursor.execute(sql_check_etat)

						############### VERIFIE QUE LA CONDITION EST VRAI ET EXECUTE L'ACTION

						#for row_etat in cursor.fetchall():

						#if row[0] == 1:

						#if NbAnd > 0

						#if int(cursor.fetchone()[0]) >= NbAnd+1 or NbAnd == 0:

						bTimer = False;
						if int(cursor.fetchone()[0]) >0:

							Len_Actions = range(len(Actions))

							for row_Action in Len_Actions:

								BChange_Status = False;
								Split_Actions = Actions[row_Action].split("=")
								Device = Split_Actions[0]
								if len(Split_Actions) >1:
									Actions_Device = Split_Actions[1]									
									Actions_Device = Actions_Device.replace("On",'1').replace("Off",'0').replace('\"','')
								ID = Device.replace("commandArray[","").replace("]","")


								if "FOR" in Actions_Device:

									tbtimer = Actions_Device.split("FOR");

									Actions_Device = tbtimer[0];

									bTimer = True;



								sql_Type_device = "SELECT Type_Device.Type, Device.CarteID, cmd_device.DeviceID,cmd_device.Etat,cmd_device.Value,Sensor_attached.value, cmd_device.DATE,cmd_device.ID, cmd_device.Request FROM cmd_device INNER JOIN Device on Device.ID = cmd_device.Device_ID INNER JOIN Type_Device ON Device.Type_ID  = Type_Device.ID INNER JOIN cmd_device as Sensor_attached on Sensor_attached.ID = cmd_device.sensor_attachID WHERE cmd_device.ID ="+str(ID)+";"

								cursor.execute(sql_Type_device)

								result_sql_Type_device = cursor.fetchone()

								Type_Device = result_sql_Type_device[0]
								CarteID = result_sql_Type_device[1]
								DeviceID = result_sql_Type_device[2]
								Etat_Actuel = result_sql_Type_device[3]
								Etat_Value = result_sql_Type_device[4]
								value_sensor_attached = result_sql_Type_device[5]
								Last_Action_Date = result_sql_Type_device[6]
								ID = result_sql_Type_device[7]
								Request = result_sql_Type_device[8]
								if Type_Device == "Plugins":
									ConditionsId =  Conditions.replace("device[","").replace("]","").split("==")[0]
									sql_Date_Conditions = "Select Date from cmd_device where ID = "+ConditionsId
									cursor.execute(sql_Date_Conditions)
									result_sql_Date_Conditions = cursor.fetchone()
									Last_Date_Execute_Conditions = result_sql_Date_Conditions[0]
									if Last_Date_Execute_Conditions > Last_Action_Date :
										Request = json.loads(Request)
										RequestUrl =""
										RequestData=""
										val = ""
										try:
											RequestUrl = Request["url"]
										except:
											pass
										try:
											RequestData = Request["data"]
										except: 
											pass
										if RequestUrl != "":
											exec_cmd = urllib2.urlopen("https://localhost/new/"+RequestUrl, RequestData)
											BChange_Status = True
								elif Etat_Value != Actions_Device :

									if Type_Device == "Chauffage":

										if float(value_sensor_attached) < float(Actions_Device):

											act_chauff = 1

										else:

											act_chauff =0
										if (float(Etat_Actuel) != float(act_chauff) or float(Etat_Value) != float(Actions_Device)):

											BChange_Status = True

											val = str(CarteID)+"/"+str(DeviceID)+"@"+str(Actions_Device)+":"+str(act_chauff)+"\n"

											#print val

											written = ser.write(val.replace(' ',''))

									else:
										if (float(Etat_Actuel) != float(Actions_Device) or float(Etat_Value) != float(Actions_Device)):

											BChange_Status = True

											val = str(CarteID)+"/"+str(DeviceID)+"@"+str(Actions_Device)+":"+str(Actions_Device)+"\n"

											#print val

											written = ser.write(val.replace(' ',''))

								elif Etat_Value == Actions_Device:

									#print Etat_Value +"//" +Actions_Device

									#print "bTimer = " + str(bTimer)

									if bTimer == True:

										Last_Action_Date = datetime.datetime.strptime(Last_Action_Date,"%Y-%m-%d %H:%M:%S")

										Next_Action_Date = Last_Action_Date  + datetime.timedelta(minutes = tbtimer[1])

										if datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"%Y-%m-%d %H:%M:%S") >= Next_Action_Date:

											if Type_Device == "Chauffage":

												c = str(int(not Etat_Value))

											else:

												BChange_Status = True

												val = str(CarteID)+"/"+str(DeviceID)+"@"+str(int(not Etat_Value))+":"+str(int(not Etat_Value))+"\n"

												written = ser.write(val.replace(' ',''))



								if BChange_Status == True:

									now = datetime.datetime.now()

									now = now.strftime('%Y-%m-%d %H:%M:%S')

									cursor.execute("INSERT INTO Log (DeviceID,DATE,ACTION,Message) VALUES (%s, %s, %s, %s)", (ID, now, val, "Scenario: "+ScenarioName+" " +str(CarteID) +" " +str(DeviceID) +" " +str(Actions_Device)))

									try:
										url = "http://notify8702.freeheberg.org/"
										data = {}
										data['id'] = 'thibault'
										data['notif'] = "Scenario : "+ScenarioName
										data['id_notif'] = XmlID
										url_values = urllib.urlencode(data)
										full_url = url + '?' + url_values
										urllib2.urlopen(full_url)
									except IOError,e:
										pass

								time.sleep(1)

								#print val

				############  SI MEME SCENARIO    ###############

				elif XmlID == Old_XmlID:

					print "Old_XmlID"

	except KeyboardInterrupt:

		print "Bye"

    		sys.exit()