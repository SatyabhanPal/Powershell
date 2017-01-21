<#
.DESCRIPTION
This script can be used for AWS windows instance and publish the memory related metrics to CloudWatch
.NOTES
    PREREQUISITES:
    1) Download the aws powershel moudule from https://aws.amazon.com/powershell/
    2) Obtain Secret and Access keys from https://aws-portal.amazon.com/gp/aws/developer/account/index.html?action=access-key
#>
[CmdletBinding()]
param(
[switch]$memory_utilization,
[switch]$memory_used ,
[switch]$memory_available, 
[Parameter(Mandatory=$True,Position=1)]
[string]$access_key,
[Parameter(Mandatory=$True,Position=2)]
[string]$secret_key
)

#checking if AWSPowerShell module install or not
if ((Get-Module -ListAvailable -Name AWSPowerShell) -eq $null){
	write-error "Please install the AWSPowerShell module from https://aws.amazon.com/powershell/"
	exit
}else{
	Import-Module -Name AWSPowerShell
	write-host "Imported module AWSPowerShell successful"
}
if(($access_key -eq $null) -or ($secret_key -eq $null)){
	write-error "Please provide the value of AccessKey and SecretKey"
	exit
}
#checking if any option is provided by user
if ( !$memory_utilization -and !$memory_used -and !$memory_available)
{
	write-error "Please specify the memroy option to be published"
}
$instanceid=(Invoke-WebRequest -Uri "http://169.254.169.254/latest/meta-data/instance-id").content
if($instanceid -eq $null){
	write-error "Failed to get the instance id"
	exit
}
while(1){
#calculating the memory using WMI 
[long]$mem_avil_report_from_wmi = (get-WmiObject Win32_OperatingSystem | select -expandproperty FreePhysicalMemory)/1024
[long]$total_phy_mem_report_from_wmi = (get-WmiObject Win32_ComputerSystem |  select -expandproperty TotalPhysicalMemory)/1048576
[long]$memory_utilization = (($total_phy_mem_report_from_wmi - $mem_avil_report_from_wmi)*100)/($total_phy_mem_report_from_wmi)
$memoryused=$total_phy_mem_report_from_wmi - $mem_avil_report_from_wmi
$metrics=(@{"value"=$memory_utilization;"metricname"="MemoryUtilization";"namespace"="Windows";"unit"="percent"},
		@{"value"=$mem_avil_report_from_wmi;"metricname"="MemoryAvailable";"namespace"="Windows";"unit"="Megabytes"},
		@{"value"=$memoryused;"metricname"="MemoryUsed";"namespace"="Windows";"unit"="Megabytes"}
		)
write-host "Press Ctrl+c to stop script"
foreach($metric in $metrics){
	write-host "==========================="
	write-host "Putting the metrics for"
	write-host $metric.value
	write-host $metric.metricname
	write-host $metric.namespace
	write-host $metric.unit
	write-host "==========================="
	$dimension = New-Object Amazon.CloudWatch.Model.Dimension
    $dimension.Name="InstanceId"
    $dimension.Value=$instanceid
	$metricdatum = New-Object Amazon.CloudWatch.Model.MetricDatum
    $metricdatum.Timestamp = (Get-Date).ToUniversalTime()
    $metricdatum.MetricName = $metric.metricname
    $metricdatum.Unit = $metric.unit.tostring()
    $metricdatum.Value = $metric.value.tostring()
    $metricdatum.Dimensions=$dimension
    Write-CWMetricData -Namespace $metric.namespace -MetricData $metricdatum -SecretKey $secret_key -AccessKey $access_key
}
sleep 30
clear

}



