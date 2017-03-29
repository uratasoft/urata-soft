################################################################
#!powershell
# SCRIPT NAME: chkNetWork.ps1
# PURPOSE: To check the network setting
# AUTHOR: NetOne T.Urata
# WRITTEN DATE: 2017/02/22
# WANT_JSON
# POWERSHELL_COMMON
################################################################
$params = Parse-Args $Args;
$Ok= Get-Attr $params "RES_OK" $FALSE;
$Ng= Get-Attr $params "RES_NG" $FALSE;
$No_Arg= Get-Attr $params "NO_ARG" $FALSE;
#
$Inf_Alias = Get-Attr $params "INF_ALIAS" $FALSE;
If ($Inf_Alias -eq $FALSE){
    Fail-Json (New-Object psobject) $No_Arg ": INF_ALIAS"
};
#
$Ip_Address = Get-Attr $params "IP_ADDRESS" $FALSE;
If ($Ip_Address -eq $FALSE){
    Fail-Json (New-Object psobject) $No_Arg ": IP_ADDRESS"
};
#
function getIp() {
   $err = "could not get IP Address!"
   $mess_ip = " || IP ADDRESS : "
   $mess_adap = " || ADAPTER : "
   $mess_domain = " || DOMAIN : "
   $mess_dns = " || DNS : "
   $mess_mac = " || MAC ADDRESS : "
   $mess_ifd = " || INTERFACE DESCRIPTION : "
   $mess_dhcp = " || DHCP : "
   $mess_conn = " || CONNECTION STATUS : "
   $mes=New-Object System.Text.StringBuilder
   $ret=""
   $domain = Get-WmiObject Win32_ComputerSystem | %{$_.Domain}
   $message=$mes.Append($mess_domain + $domain + $mess_adap + $Inf_Alias).ToString()
   $dns = Get-DnsClientServerAddress -InterfaceAlias $Inf_Alias -AddressFamily IPv4 | % { $_.ServerAddresses }
   $message=$mes.Append($mess_dns + $dns).ToString()
   $mac = Get-NetAdapter | Where-Object { $_.Name -eq $Inf_Alias} | %{ $_.MacAddress }
   $message=$mes.Append($mess_mac + $mac).ToString()
   $ifd = Get-NetAdapter | Where-Object { $_.Name -eq $Inf_Alias} | %{ $_.InterfaceDescription }
   $message=$mes.Append($mess_ifd + $ifd).ToString()
   $dhcp = Get-NetIPInterface | Where-Object { $_.InterfaceAlias -eq $Inf_Alias } | %{ $_.Dhcp }
   $message=$mes.Append($mess_dhcp + $dhcp).ToString()
   $conn = Get-NetIPInterface | Where-Object { $_.InterfaceAlias -eq $Inf_Alias } | %{ $_.ConnectionState }
   $message=$mes.Append($mess_conn + $conn).ToString()
#
   try {
       $ipa = (Get-NetIPAddress | where{$_.InterfaceAlias -eq $Inf_Alias}).IPAddress
       if ($ipa -eq $Ip_Address) {
           $message=$mes.Append($mess_ip + $ipa).ToString()
           $message=$mes.Append(" " + $Ok).ToString()
           $result = New-Object psobject @{changed = $FALSE; $ret=$message }
       } else {
           $message=$mes.Append($mess_ip + $ipa).ToString()
           $message=$mes.Append(" "+$Ng).ToString()
           $result = New-Object psobject @{failed = $TRUE; $ret="$message invalid value detected!" }
       }
   } catch {
       Fail-Json (New-Object psobject) $err
   } finally {
       Exit-Json $result;
   }
}
#
getIp
