import requests


urlmax='https://cns-mx76av.cfms.org.uk/maxrest/rest/os/mxmeterdata?_actio=AddChange&ASSETNUM=BRI-MO-01&METERNAME=HUMIDITY&_lid=rotarua&_lpwd=Rollsroyce1&SITEID=BEDFORD'

#r=requests.get(urlmax)

r=requests.post(urlmax,data={'NEWREADING':'44'})

print(r.url)
