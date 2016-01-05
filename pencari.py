def cariPemain(pemain,cari):
    found = 0
    for i in range(0,len(pemain)):
        if pemain[i]['id'] == cari:
            found = i+1
            return found
    return found

def cariUsername(pemain,idPemain):
    for i in range(0,len(pemain)):
        if pemain[i]['id'] == idPemain:
            return pemain[i]['username']

def cariRoom(pemain,idPemain):
    for i in range(0,len(pemain)):
        if pemain[i]['id'] == idPemain:
            return pemain[i]['room']    
