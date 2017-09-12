<?php
require_once dirname(__FILE__)  .'/../../../Security.php'; 
require_once dirname(__FILE__) .'/../../../ListRequire.php';
require_once ('Livebox.class.php');
?>

<div> <!--/* class="DeviceDetail Corner"*/-->
	<img id="Livebox_pic" src="Core/plugins/Livebox/pic/Livebox.png">

	<table class="table table-borderless WidgetContent">
		<tbody>
			<tr class="WidgetStatus-center">
				<td id="Contentcmd_<?php echo CmdDevice::GetCmdId('Up',$Device_id)->get_Id()?>">
					<img src="Core/pic/temp_up.png"/>
					<span id="InfoDeviceUp_<?php echo $LieuxWithoutSpace ?>_<?php echo CmdDevice::GetCmdId('Up',$Device_id)->get_Id()?>"></span>
				</td>
				<td id="Contentcmd_<?php echo CmdDevice::GetCmdId('Down',$Device_id)->get_Id()?>">
					<img src="Core/pic/temp_down.png"/>
					<span id="InfoDeviceDown_<?php echo $LieuxWithoutSpace ?>_<?php echo CmdDevice::GetCmdId('Down',$Device_id)->get_Id()?>"></span>
				</td>
			</tr>
		</tbody>
	</table>
	<table class="table table-borderless WidgetContent">
		<tbody>
			<tr class="WidgetStatus-center">
				<td id="Contentcmd_<?php echo CmdDevice::GetCmdId('Last Change',$Device_id)->get_Id()?>">	
					<img src="Core/pic/Synchronize.png"/>
					<span id="InfoDeviceLast_Change_<?php echo $LieuxWithoutSpace ?>_<?php echo CmdDevice::GetCmdId('Last Change',$Device_id)->get_Id()?>"></span>
				</td>
			</tr>
		</tbody>
	</table>
	<table class="table text-center table-borderless WidgetContent">
		<tbody>
			<tr class="WidgetStatus-center">
				<td id="Contentcmd_<?php echo CmdDevice::GetCmdId('Reboot Livebox',$Device_id)->get_Id()?>">
					<div class="btn btn-primary pull-left" data-i18n="Edit" data-theme="a" id="rebootLivebox">Reboot </div>
				</td>
				<td id="Contentcmd_<?php echo CmdDevice::GetCmdId('Update Livebox',$Device_id)->get_Id()?>">
					<div class="btn btn-primary pull-right" data-i18n="Edit" data-theme="a" id="UpdateLivebox">Rafraichir </div>
				</td>
			</tr>
		</tbody>
	</table>	
</div>

<script>

	function loadData()
	{
		var request = $.ajax({
			dataType: "json",
			type: "POST",
			url: 'Core/plugins/Livebox/Desktop/Livebox.class.php',            
			data: {
				act: "loadData"
			},
			cache: false,
			async: true
		});

		request.done(function (data) {
		});

		request.fail(function (jqXHR, textStatus, errorThrown) {
		});

	}

	$("#rebootLivebox").click(function(){
		var request = $.ajax({
			dataType: "json",
			type: "POST",
			url: 'Core/plugins/Livebox/Desktop/Livebox.class.php',             
			data: {
				act: "rebootLivebox"
			},
			cache: false,
			async: true
		});


		request.done(function (data) {
		});

		request.fail(function (jqXHR, textStatus, errorThrown) {
		});
	})

	$("#UpdateLivebox").click(function(){
		loadData();
	})

	loadData();

</script>
