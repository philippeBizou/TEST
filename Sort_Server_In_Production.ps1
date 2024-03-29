#########################################################################################################
#                                                                                                       #
#            Fonction du script	: Vérifie la présence des serveurs dans la CMDB                         #
#            Serveur statut "in production" et present dans la CMDB                                     #
#                                                                                                       #
#                                P.Bizouard  / SOGETI    Version : 1.3                                  #
#                                                                                                       #
#########################################################################################################

# '---------------- Déclaration des variables ----------------'


$pathExportDB = "C:\temp\computer_status_export.csv" #  Chemin où est stocké le fichier
$pathCMDBFile = "C:\erwcsa\scripts\Item_Export.csv" #  Chemin où est stocké le fichier de référence de la CMDB
$FileName = "C:\temp\server_In_production.csv" # Chemin où est stocké le fichier trié avec les serveurs uniquement en production

# '----------------Test si le fichier de sortie existe, si c'est le cas le supprimer.------------'

    if (Test-Path $FileName) {
      Remove-Item $FileName
    }

# '---------------- Mise en forme fichier CMDB selection des assets en Production ----------------'

$ServerList =  Import-Csv -Path $pathExportDB -delimiter "," -Header server,revision,duration,product,date
$CmdbServerList = Import-Csv -Path $pathCMDBFile -delimiter "," -Header A,B,C,D,E,F,G 
$CmdbServerInProd = $CmdbServerList | Where-Object {$_.F -eq "In Production"}
$CmdbServerInProdList = $CmdbServerInProd | Select-Object C -expandproperty C



# '---------------- création du fichier de sortie selectionnant uniquement les serveur en Production ----------------'

foreach($server in ($serverList | Select-Object -Property server -expandproperty server)){
  
 if("$CmdbServerInProdList".Contains("$server".ToLower())){
          
      $row = $ServerList | Select-Object server, revision, duration,product, date | where {$_.server -eq $server}                                  
      "{0},{1},{2},{3},{4}" -f $server, $row.revision,$row.duration,$row.product,$row.date | Add-Content -Path $FileName             
     }
}

 if(!(Test-Path $FileName)) {
      New-Item $FileName -ItemType file
    }