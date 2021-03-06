<?php require_once '../Core/Security.php';  ?>
<div id="scheduler-here" class="dhx_cal_container" style='width:100%; min-height:90vh;'>
	<div class="dhx_cal_navline">
		<div class="dhx_cal_prev_button">&nbsp;</div>
		<div class="dhx_cal_next_button">&nbsp;</div>
		<div class="dhx_cal_today_button"></div>
		<div class="dhx_cal_date"></div>
		<div class="dhx_cal_tab" name="day_tab" style="right:204px;"></div>
		<div class="dhx_cal_tab" name="week_tab" style="right:140px;"></div>
		<div class="dhx_cal_tab" name="month_tab" style="right:76px;"></div>
	</div>
	<div class="dhx_cal_header"></div>
	<div class="dhx_cal_data"></div>       
</div>

<script type="text/javascript">	

	$(document).ready( function () {
		scheduler.config.dblclick_create = false;
		scheduler.config.drag_create = false
		scheduler.config.time_step = 0.1;
		scheduler.init('scheduler-here', new Date(),"month");

		scheduler.attachEvent("onClick", function (id, e){
			PlanningId = scheduler.getEvent(id).planningId;
			PlanningCmdDeviceId = scheduler.getEvent(id).planningCmdDeviceId;
			PlanningDate = scheduler.getEvent(id).planningDate;
			PlanningDays = scheduler.getEvent(id).planningDays;
			PlanningDeviceWidget = scheduler.getEvent(id).planningDeviceWidget;
			PlanningDeviceWidgetType = scheduler.getEvent(id).planningDeviceWidgetType;
			PlanningRepeat = scheduler.getEvent(id).planningRepeat;
			PlanningHours = scheduler.getEvent(id).planningHours;
			PlanningName = scheduler.getEvent(id).planningName;
			PlanningActivate = scheduler.getEvent(id).planningActivate;
			PlanningDeviceStatus = scheduler.getEvent(id).planningDeviceStatus;

			$("#modal-planning-data").modal("show");
			$("#text-button-save").html(" Update");
			$("#planning-device-name").html(PlanningName);
			$("#planning-cmddeviceId").val(PlanningCmdDeviceId);
			$("#planning-planningId").val(PlanningId);
			$("#planning-datetime").val(PlanningDate+" "+PlanningHours);
			$('#modal-planning-data .widgetType').hide();		
			$('#modal-planning-data #planning-delete').show();
			$('#modal-planning-data .'+PlanningDeviceWidgetType+'.widgetType').show();

			$("#modal-planning-data #active").prop( "checked", PlanningActivate);

			if (PlanningDeviceWidgetType == "Binary")
			{
				$("#modal-planning-data #action-"+(PlanningDeviceStatus==1 ?"on": "off")).prop( "checked", true);
			}
			else
			{
				$("#modal-planning-data #planning-slider").val(PlanningDeviceStatus);
				$("#modal-planning-data #planning-info-slider").val(PlanningDeviceStatus);
			}

			if (PlanningDays.length >=1)
			{
				tab_days = PlanningDays.split(",");		
				$.each( tab_days, function( key, value ) { 			
					switch (value) {
						case "0" :
						Days = "monday";
						break ;
						case "1" :
						Days = "thuesday";
						break ;
						case "2" :
						Days = "wednesday";
						break ;
						case "3" :
						Days = "thursday";
						break ;
						case "4" :
						Days = "friday";
						break ;
						case "5" :
						Days = "saturday";
						break ;
						case "6" :
						Days = "sunday";
						break ;
					}
					$("#planning-days-"+Days).prop( "checked", true);
				})
			}
		})

		scheduler.attachEvent("onBeforeViewChange", function (old_mode, old_date, mode, date)
		{
			if (old_mode != mode || $.datepicker.formatDate('dd-mm-y',date) != $.datepicker.formatDate('dd-mm-y', old_date))
			{
				Recup_Planning();

			}
			return true;
		});
	})
</script>