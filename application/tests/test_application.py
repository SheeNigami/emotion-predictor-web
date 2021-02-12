#1: Import libraries need for the test
from application.models import Entry, Accounts
import datetime as datetime
import pytest
from flask import json
 
#Unit Tests

# Insert testing predictions in class Entry
@pytest.mark.parametrize("entrylist",[
    ["23 Sep 2020, Surprise by chad1","Surprise","chad1"],
    ["23 Sep 2020, Fear by chad2","Fear","chad2"]
])
# Test Entry Class
def test_EntryClass(entrylist,capsys):
    with capsys.disabled():
        now = datetime.datetime.utcnow()
        new_entry = Entry(  image_name= entrylist[0],
                            prediction= entrylist[1],
                            username = entrylist[2],
                            predicted_on = now  ) 
 
        assert new_entry.image_name == entrylist[0]
        assert new_entry.prediction == entrylist[1]
        assert new_entry.username == entrylist[2]
        assert new_entry.predicted_on == now


# Expected Failsure testing for Entry class (range testing)
@pytest.mark.xfail(reason='unexpected values in label encoded fields')
@pytest.mark.parametrize("entrylist",[
    ["23 Sep 2020, Surprise by chad1","WEWEWEWEW","chad1"], # Test wrong data input
    [-1, -2, -3, 4.2], # Test wrong datatype
])
def test_EntryClassFail(entrylist,capsys):
    with capsys.disabled():
        now = datetime.datetime.utcnow()
        new_entry = Entry(  image_name= entrylist[0],
                            prediction= entrylist[1],
                            username = entrylist[2],
                            predicted_on = now  ) 
 
        assert new_entry.image_name == entrylist[0]
        assert new_entry.prediction == entrylist[1]
        assert new_entry.username == entrylist[2]
        assert new_entry.predicted_on == now


# Unit test for Accounts Class
# Validity Testing
@pytest.mark.parametrize('userlist', [
    ['asdfasdf', 'lskdjfsldkfjksdl'], # Valid user
    ['sheen', 'sheenhern'] # Valid user
])
def test_UserClass(userlist, capsys):
    with capsys.disabled():
        now = datetime.datetime.utcnow()
        new_user = Accounts(  username= userlist[0], 
                          password = userlist[1],
                          created_on = now  ) 
 
        assert new_user.username == userlist[0]
        assert new_user.password == userlist[1]


@pytest.mark.xfail(reason='user already exists')
@pytest.mark.parametrize("userlist",[
    ['sheen', 'sheenhern'],
    ['asdfasdf', 'lskdjfsldkfjksdl']
])
def test_UserClassFail(userlist, capsys):
    with capsys.disabled():
        now = datetime.datetime.utcnow()
        new_user = Accounts(  username= entrylist[0], 
                          password = entrylist[1],
                          created_on = now  ) 
 
        assert new_user.username == userlist[0]
        assert new_user.password == userlist[1]


# Test add API (range testing)
@pytest.mark.parametrize("entrylist",[
    ["23 Sep 2020, Surprise by chad1","Surprise","chad1"],
    ["23 Sep 2020, Happy by chad1","Happy","chad1"],
    ["23 Sep 2020, Fear by chad2","Fear","chad2"]
])
def test_addAPI(client, entrylist, capsys):
    with capsys.disabled():
        data = {  'image_name':entrylist[0],
                        'prediction':entrylist[1],
                        'username':entrylist[2] }

        response = client.post('/api/add', data=json.dumps(data), content_type="application/json")

        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"
        response_body = json.loads(response.get_data(as_text=True))
        assert response_body["id"]

# Test get API (get added entries)
@pytest.mark.parametrize("id", [1,3])
def test_deleteAPI(client, id, capsys): 
    with capsys.disabled():
        response = client.get(f'/api/get/{id}')
        ret = json.loads(response.get_data(as_text=True))
        assert response.status_code == 200
        assert response.headers['Content-Type'] == "application/json"

# Test getAllEntry api
@pytest.mark.parametrize("name", ["chad1"])
def test_getAllEntryAPI(client,name, capsys):
    response = client.get('/api/getall/<name>')
    ret = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert response.headers['Content-Type'] == "application/json"

 # Test delete API (Delete added entries)
@pytest.mark.parametrize("id", [1,3])
def test_deleteAPI(client, id, capsys): 
    with capsys.disabled():
        response = client.get(f'/api/delete/{id}')
        ret = json.loads(response.get_data(as_text=True))
        assert response.status_code == 200
        assert response.headers['Content-Type'] == "application/json"
        response_body = json.loads(response.get_data(as_text=True))
        assert response_body['result'] == 'ok'



# Test predict api (consistency testing, always Neutral)
@pytest.mark.parametrize("image",[
    ['data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBxMTEhUTExMVFRUXFxUXGBUXGBUYFRYaFxcXGBgXGBcYHSggGBolGxcWITEhJSkrLy4vFx8zODMtNygtLi0BCgoKDg0OGhAQGy0lHSUtLS0tLS0tLS0tLS8tLS0tLS0tLS4rLS0tLSstLS0tLS0rLS0tLi0tLS0tLS0tLSstLf/AABEIAPsAyQMBIgACEQEDEQH/xAAcAAABBQEBAQAAAAAAAAAAAAAFAQIDBAYABwj/xABTEAACAQMCAgYFBgYQBQEJAAABAgMABBESIQUxBhMiQVFhFDJxgaEHQlKRsdEjYnKTosEVFjM0Q1NUgpKjs9LT4ePwJHWDssJECCVjc6S0xdTi/8QAGgEAAgMBAQAAAAAAAAAAAAAAAQMAAgQFBv/EADIRAAICAQMBBAgHAQEBAAAAAAABAhEDBBIhMRNBodEFFBVRUmGRsSIyQnGBwfDxciP/2gAMAwEAAhEDEQA/AMpSgUlPhQlgACTzwATsOZ27q9I3SOSjTcW6AXsAJ0LKNz+CJZsD8QgMfcDWXIr3bjEyrxKzLMFHU3YySAN+p239nwryPptLG1/cNEQULjdcYJ0rrIx+PqrJptRLI6l7r8aH5ccY8oCV1PiOGBABII2IyDvyI7wfCte1nej1rCxU4Bw0dqrb8sqzgj31onPb/wBoVGNmNrq9A4LZZkPp1tYR2+htTr6Org47OkxuTnNefseePPGefvqQyKTaJKNHV1bTpa0dk8MMVtbMOoR2eWJZHZmJySzez41l7y6adlAijU8gsMYTUT+KvrGpDJuV1wGUUnRWWnrRY8MjtxquyS+Mi2jYa/8ArPuIh5DLeQoh8oFlFFdKsUaxqYIm0qMDJL5PmdhvQWVOSivr+xScGo2ZsVJUYqSnLqZZdB9OSm05KuZpDqcKbThTDFkHV1dXVBR1dXV1Qh1dXV1Qh1dXV1QgNtmUOpddSBlLKDgsoIyue7IyM1urjpTZ9S0dtrtVZCpjS3j1ucEYaYueydgds+dYHrott5NwD6q9/wDOrrmeJOZkP81f71cfJn0+Rq5f76Hs46TUR6R+3mew9IuL28k0EiXFpoEU2ZJQJdHah9SMEHrPAHzrM8W6RWrwyRIhu3Kk9dOkMQTbGYgihts5A29tYbhrRzOUTWGClhlVwcEDHredNvpoosai/mAEOD59qkQnpout/P7EyRyrqiawlCSxuQSEdGIHMhWBIHntV7pPfrc3Us6qQshUgNjUMIq74JHzfGgttxKFj/ChRjLaFIGfIPk+6pJ7+Fc4aQgcjpUavYC1avXNPuu+f5Edhkqq4Hqgzvy78c/dRgxcP+le/wBC3/v0CtL6N+6RdmOWCAbDP0qhj4vCe6UfzU/v1JazDL9QFimu40vS3jIu5xIqFEVEjUEgthc7tjbOSafwPjy28ZUW6s7ZBmDukuD81WXdBjbs4zUXDOFxzKWErADv0A7+Gz0St+iiO2kTkf8ASH9+kS1+jUdjlx/JZYsre5L7Aw8Qtf5Cv5+eiPSzj0F3IrpCykIily3awurshQSuNxvzq+Ogi/yk/mv9SnftHT+Vf1X+pQ9oaO0974/9EeDNVV9jH4GTjOM7Z547s04CtkvQZCP31/Vf6lKvQlP5V/Vf6lM9q6T4/B+Qh6LM+77GOqRRWyXoPH/K/wCq/wBSmt0MQf8Aqc/9L/Uq/tfR/H4PyES9H53+nxRkMUoFa2TolGBn0k/mh/iVQk4NEuczP+bG/n+6Vdel9J8fg/Iy5PRuo+HxQDpcUT9Dg/jX/Nr/AIlKLOHl1sn5tf8AEq69KaV/q8H5Gd+jtR8PivMF4rqMLw2E/wAM4/6S/wCJSz8LhUZM7+zqlz/aU1a7TvpLwfkD2fqPh8V5gWuogLaH+Mk/NJ/i0vosP8ZL+aT/ABaPrmH4vB+QfZ+o+HxXmDq6r5tof4yX80n+LSejw/xkn5pP8Wp65h9/g/Ins/UfD4rzMLxufQqMPoL9lW7fonxW4jjljs5GR1DKwMeGUjIIy2aG9Ic9WnhoX7BXtcU6rwjhmriR4f8AgIu2Ah6z8GvZ7XhzrzaPcZskk+DyV+DcQ4ePSLi1kjjxoLnSygsRjOknGTtk+VPvbO7la31WcjG5XXAAAetXCksAp2GGUktgAHevUr51m4NxJE4kOIMsRcuQo6tVXVp7Pj1bEedE+iA34N/yqb/8fVXBN2ZnJvqeW8I6I8Uhcn9jnAJyMGEldsYGWoB0yab0hllR42TC6GGkrsCfrznI2PdWi6L9K766uXhm4ybNFRnEsoh0syuq9WNRQZIYnn800vyuWk63pW6uUkb0aJ8pF1QYdZMFTTrbJByc57xttVXCKe4nUynRzhl5dEm0gkmMeCSMaUzyGW2DH66JT/J9xdjkWMgHhqj/AL1afoTxOS26N388DGORbuPDLjUATZq2MjvDMPfWQk+Uzifdezf1fu+bTEl1AGOj8l3DAZJIJFgSQxFxo0rIG0FTg5zr25VdtekNxLOIbWJpJWBOhdIYgDJPaIFaPolaRXfR5hdXQt1e5d3nbT63XBt8kDJb7asfJ30U4fBfpNb8VjupQsgES9XkgrgnssTsN6U8EXK6CnRBwDjUzRGSWKRUEhiL4GlZA2gocHOdRA5YoHJ0hu5bk29tE0smCdC6QcLzPaIHeKOi56vgt055LxJz/wDWJWf+SG46zjWruMM3/hVPV4KfQtudBPg3SG66hp5YJBCrMrS9korK2lg2DkANsTjA55xvQ+26RXdxO0NrE0zhS5VSoIUEKW7RAxllHvrWdGePJZ8JaWWPrImvriOVMZ7EkzqxC/OwN9PeMjvqXoL0MFnxVrm2brLG4tHMLg5CFpYGEee9dIyp8Bg7jJt6vCwb2Yfg/FuJ3YZra2llVTpZlwFB+jqYgE+IGcZGeYq/cvxeKNpJLKYIoLM3YbAHM4VicDyFNTjM9p0cglt5Wic3sqll05KkznG4O2Qv1UZ+Ta5v72ISjjUZlZZNVpJDHK8arJpDlVkVhnA3Ix26Pq+P3E3Mp8J428ltHNIjiOVmSOTHYd0DkqCDn+Dk5jHZrOycVurqWSO3haVolLsFK9lQcZOoiicV0I+jnDHPIXc3xW+H66i+RiTVd37eNo//AHiqLTwUugG7QF4Nb8Su4+tt7WSSPJAcaQpI54LEZx5UZh4fxCBTJdWksca+tIdLKo8W0MSB4kjA7zR3oj0jtpuE2sCcVHD5YcrJnQGbBbbEmxU5DZGfDnmiRWd7a69F42l8VhcvEyQv2NLZUFGGhmGQCcimvFEo4o874zxeRZFjjBLMQqgcyzHAA9pIq/Ba34MvW2kg6lQ0pGhiilSwYqGJIwCdgeRoJcfv21/+fb/2qV6D0p6QNYcea4JJgaOGKdd8aGU9vHeUOG9mod9HHxEqopoxfFuM6ANO5NEuGPN1Mc0kTrHK2mOQ40ucMeyM5OyMc45DPLerHFPk4Y8XS2j2tJgZkcHIjhGOsQHPNWZUXykQ9xo/xm4S5lzEFW3gXqLZVGF0rgSSAcsEqFXu0xgj1jTd4HBJAVzUeKnnh01DtTbQsyctqJIVz3IPgK10PTdEtLW2uOFwXSwosaNJMDkqoXVoaA6SR3ZPtrL25/BD6vrAqDVnR5HFZ0ztTxRlyzUP09ieGWztuGQWYugIZJI3B7LZU9hYky2lmAJO2c4PKjXDuNXcLWWIYf8Ag7Z7cgysfSFYQjOeqHUnMIb5/PHnXlsZ0yK3g6n6mzW+45EzSxqJY4gzAa5W0Rr5s2DgfeKRlnNSSj3mTLBR6FninSKygGqXgnDgTyHWqWY+Q9FrE9MulbcQmed4lXspGiBiwjVdRyTga2yz74A35bVDc2QuOI28UjZSW5igLI2QVaUIzRtjcEbg47xW34h8k0BtZDaSSelLNcrHFI66ZlgldCg2GH0gHOcZG+AchkbcfxCTNdE+n0dnby20lnHdQTMsjRuwVQ4Cgk5RgwPVo2MDBFGIenPD2xjgFlv4yR//AK1BeDdE7T0C3u7pbnU15JbypGVDBVhmYBVcDDB0XOTyzWgPRrgSWkN6P2R6uaR4kAaHXqXXnIOwHYPf4VfuIdwnjZFr6EYYo4zcmfWJT2AZOtEYj6sAgernUPHHdXdH7kx8U6+3VJSiuNLyGMEFNJIYI+4J5YqLh/Rrhi2kd3O16yzy3IiVGhBSOGV0UPrwC2lQSQeZ5bVe4bweyRLS8sXuernmlt2ScoWyI5W1DTy3iIxk51DljdMlJXK+iLRrvLfDuL+jwy28sNrdRTSvM0MshVY3dtRUHqWEq5AIJVSCD4gCSw6WwQSarfhdhBJgqJEm3AP5NspI8sjPlQs9HrAzrHd+ma5p0jiaFohFiTQq6s9odtmztypL7oxwsXcdnGb8Sm4WHWzQ9WcPiTBA1cg2CRzowcmk7AxGu2Wx9DYRtGJjO0/WMHYsSxHU9Xgdpj8/7qk6KdNH4crRxhJ4WOpYnkMfVMSSxRgj5DZ3XHMZHM5AcV6P3xumthaXbQC5aIS9TJvCJiofWE0nsYOrl31oV+TuxWXiOtb6VLWS3RI7ch5mEsUbHshe1hnJ8gPKpGM7tspTO6PcXWGyW1ktLW+iDmUCRyuh2BLDBicN2mfDbHDYxVq16ZxQF/RuGWVrKyMnWpICVBxzVbddYyAdOoZwNxQ79jLOLQkEPE4Xdv8A1kaIjKPWxqAYkal9XxGaH9H+BWk/7IT3huNFsYMCFkDHrWkU7MMHcL3jvoXPdtsPNhrgXFY7ezSye2tb2CN2ePr5NBUsWJyvUyBjl3w22zYx3mzH0qiiWRbbh9javIjRmWOXJUMOZRbdNeOeCw5UAk4Dwy4tb17KS+SW1h649cYijAauzhc89J7xjbnyovf9B+HwdWrW/GJi8Uche3QSxZYHK6guxGOXmKsozrqEZadJo4bWOzms7W9ihJ6syyaSoJOAVMTgsMkagRkd3i4dM4limituH2lmZkMbSxSAsAQRnQIFDEZOMnGfHlQ/hvRrhcqX1ww4iIbVoU6vsekamJVwUxzDY2OCMGutui/CbiG4lg/ZKM2ypK/XCMa01dtEH0ioYA5GCQd+VFKddQMFStFrSQFSyOjqCcA6HVgM4OM6cZwffRni3ExfzSTSIkZcINCuZAAi4zqKLz8MVJZ9GOCSW010v7I6IZUiZS8Oss+nGkcsdsd476o23AIjaXV3w5LuQx3SQxxEB3KGKIuWSNSSQ7ucg8sVVQaVJldroN2fSyeGzNgpQKAUW46wiWOIndBHowWC6kVtQwNJwSu9aLikKgKrKAAAANgANgAPCs9bdFZnsr66uorm3liMAhEitEjdY+lyQ65YDI5cs1peK9BOHW0hia341OyhcywRB4nJUE6WC47+Xcas4N9WRxvqSyIJACD/AJ0v7Gj/AGaiiihilkiheV40K465HjlUlQSjq6qcjOc6Rsw58yQ9IHgaRLNOLoCS7zAWgGkKeelD+iKqyjmPBh9oNS8Rtz2GXvUA+WAKqyybZ8R8RtWnadhStIrXq4Zh5n7a2z26zmBpWdEwnWMg1MFK5yBg5OcdxrGcV/dPbWw4RKTBH+SB9W1Iz8JMx6l0rHjhi9fa3AJKwXMMhyO0Y0mUlio+doGce6jnHeJCZYeoeSOSK7u51cKylRJK7RkE7HKtuvgSCO6qVpHqOnuolaWRBwcY+NZvWJRVIyxbYvSni0d1aRL1fVzCczTaVIjZhbzRmRSdsMSnZ5775wTWdtXjk4TFaDJlge4nYaTpCkyFSG5E9tRgeNaLidqBHIfxH/7TWe6Jx6pJF+lBIP8Atp+LI5ptmjHC2GH4ZZScPht7uS5iSB5pFkhVWDrcOzj5rEY6zTggbjPKm3Ato7OzhsmmkhhvOsaWYBTl1kQoBpUk/hc5xjA55qneXOeHx7+t1a/0T/8AzUkC/wDu1T3+kLj84o/VRWSTg7/YtDGm2XOIW2Z4JjnEU8EpxucJKjNgd/ZB2qGV1N8t2Q2hbwyDsnVo1kk6efLJxzoncuoGG7+6hcTErIvghI9uazY8jSr5meb5JJOMXkkrSRXM4X0iVxHqO8XXsYwEPL8FpGOfvovHxiHruIlpbm3W5lgaKWJD1uIoo0bAKnT2kK7jcHas3wwHrUxz1Cn8VnzI3kSPqpyzyQre6L3EIYZTHIl7fXLxnlcKoRUbBcg9Wu/ZXvqnwaG0RL+G5klSK7W3w8aFmBjeVmA7LAc05jvqXhB/dCfVCHPvqq0/gowOW1Dtnusm/vLFvw6wtbW8js5LqaS7h6j8Mqqq51drOhdhqO25O1ae6u45hEwveIW+mKNDHCoCZUbt2o233xnPcKyOsE5JwfDu9tGre7BTSO4DNR6ma7kXjKyLhEnoQvVtJbhpLiW2dJpUQuS0g9JZsqFGFZz2h7M07i3FbmVGiluJHQ+smIVDYORkxxq2nIG2cHkcjaobrbl9dUcsSRg8s+7xpU9RKXfRPxN1FEHD9EVjc23a1zXMMq7HTpUx6styHqHY1NwC/a2tJ4I3kjlkuhKGTI/B9Sit2xsO0pGOdMMD59U8s+6om9mM8vOrx1F9H8gSjOP5k0Wbric0tle208sszTC36kOSVGmUmUa8dnshTv7qN+m2xAK8R4tANK4hz1mjYArrZHLHPfqPkcVnNVLqpizySKqbCvHb9Z7qSZAwQiNV1DDNoXBYjuyT377d3Kq/W+dUw9PyKRKW52wdQAAMDPcv2igkkROAO80XiVmC47wPsobcKVYrnBXIrqNnXiqRHxW1xg91aboxGXt1074JB8tzVK4iDR7+FP6IcR6pnhPzu0vtHMe8fZSM8bhwIzrdE2dlbrHuTlscqtddjegRnPPJz3mlEzE865zRiU64QSvZ9UbjxRufsNAeg5/4oDxjcfAVfDFiVHsoZ0M7N2gPhID7lP3Vp0/SSNOCVyK88o9FiT8dvgXoxEf+BtU+ncfY7N+qs/L+4ofxm+Jai87nRYxj5qSSH3khav0g/wBy8JbVJ/uHbl85yOQ50LhOmUHuOx9h2ohcXAC5oRpZjkA1mXBjkyxZxFLgA9xOP1VTu8l29po3IAcE7EY39lRFVJzpFDcDbwVok0258Wb4AVQzRiUhlC9wqtc2JG45YqWUaBUjb1bsMlsA71BJaMeQ3o9w+2Ead5zuAfHAznyFJz5ljj8zZoNG9RPn8q6+X+6D4oMDtHmOXMnzA8KlXHIL7M5J+GB8KYHB3znO+c5z5+dW57ouEGFGgYBAwT5k+Ocn31yZ5G7bPU48UcaUYLj/AH1ElhZQCyAAjI2I2OR3Y8KhMKNzGDyzzG/xHxqbiHHBIQskiAppGC2MdZsgOTuSQQCdzvVi5mLkEhRgAdkYzjvPnVZy28r+OCqbkqkl8+ehn7/hZQah6oGTk7nfuwMUNzWvtZFYZBDLkjI3AIJU49hBB9lBeNWJVsjJzkscdkcsbit2l1bk9k+pwtfoowXaY+nu/sGUuqm43p1dA5BQ4MMjfuTI+qgfFE7evxJB99aHg6Dqyx27IHwoVfW+rbx399dd9DrJ8luBMoPZQ2+s2Uh1PaByPdVy1DCNRy0n6xV+W3ymrx5Dx86DpoHQhsOICRc9/evgfuq7HJyoVb8MJOUyM94yMUYtrbA3JPtrBkik+DHlxJO0x4nPMbGhdvcdTca99tR259tGH2t8KLiOhHGhhlx3qfgf86GB1IGJtSIZXVYI1J35geO5BPxqe0uDI+rkEjjQD2Df4gn30DQs7HVjC4Vfpbbnf30S4Tc9W+gr2W+d9E8gPYafPG1Bl5J7WaLUGXDfDnS+kAbDYeA/XUemu6usViSd7nNSSXQGAPDn+qqnV0pgqA5JUuiSc4x7KWW7880xbcYp3UDHKhaBRJbHU2d/dV6/fSrnuVW7tXqg5Oketvk476h4SoDj2j2c6uVy9XP/AOh6b0XFLBx32Ze3gkj/AHOMgMV0SNETJEspIkTRzCiQBscsP5ZqwJroSdWusgORqKDGkzQk9ojGBE0mN/m95FFuL7QyHSWGncAE5HzthucDJx34xQPhsip1bRFW1SaCUkkeNRomMYwG0jGFyviw5HFNhPtYubS+n3LTj2clFNjOMsouJVMqFnNkqoXjDApNrZQuQcBXVsnnq591FIrO6J7bPgyJqAcA4zKrsuD2VKmEgDBypOM86Np0gkYF2gQ/gmfAVtRKwwTKuTnvkccvm0ZteJuZo4zobUuSY8tzV2DbtlFwq8w2TIBnxrl7WMEtq4Xf8kun0FxcJSbt8/3/ANG8Bt5o3cSA6CZCna2XM0jYK5wSQysG57kHkKLcSjDxHIY47l5nG4H+/Cpilcw7Lcx7OfJuXnXMeZzyb+8fLFFY3HuMcIz4UvVmrmjfy8+dO6uvR2eW2oo2KaY0XSDsCc+wUk1mrHPLyFWIB2V9g+ynYp8tTkfA/tGVGsVPjVmOMD/Pup6rTtNK7ST4sq5NjVrsU9Vp6JQKFfFA+MntgeC/aa0wjoRfcPea40RrqOlfIDnzNaNOvxlodTOt2eQ23JqRwSNtz3Y+Fau06HzrJG8jIgV0Ov1wMOpIZe9WUMvlnNAeI2waZ44m6sNKwjYA7DWdBXG/LGMVvcRt2GrRtSK3iAfvqwkVELm0ERVcgg5BblhtyQPpd+/lXdTXNy43GTRnaKawU8oKtrDvUqW2aXQCiqeVPaFjyFFI7SpzDQ2hoDW8BBzVbj9y8bKVbSCsj/NwcaCB2ufMjA3NHmj8qi6sHYgZHL7qwaqOySnVo7norUJLY+4z4vJDrxJ/CsoGYgdIdhhQV2OBzbau9JcjUspwYlcagijLNp+icePMjJ8K0dlYiVwh0jJ3yOYG57ueATvT3ssSGPKkjs9wHsy2KydqqtR7/kdZ5oKVd/X+DMrfOTtIwwjHB6oEsHcb7HV6oHZ54q/bcRy8Y6xcNESd13fKfHc7edaG84MY1U6VxpGd12O/ZA7+7lTYeGAxGTKAAjbB28e7nuvKq5HbcXDuFvUY2r7uhjk4nN1SP1pJMbyN+4kDSqHcBchRk5HrVqrk4TnjPh9Q/XXRRL4ADv2H1V0zauf1d3lQxpZ8iUY15f7gz63OowbQHEBNd6MaKlBTNNdyjzRStoV0Ly9VfsFJ6MtMt5cIv5K/YKc7E0e8Ino61zKO4U9IDVqO3qJEBojqZLY0RW2HfTtAFWqgFFLarPRBE6+5+mDGP5unu9+fhTeIX6Qrrc+xe9j4ChnQJzJdTPyyNWB5tyPj/lWvSRe6y0VxZoeltzLFE0qRBlQaiNZUkbDbA5jnv4UC6M/8TElyY11RPINyFGQurAwCSBt4b1uLuLUjDAbII0nYEHmM921A+CcCSFiQrHJ5uANI8AAdz5+VdFp2Mi47X7yLjFiFMezc8u2TzKkAfWTUQTyo3xxfwX86PH9NaDq1YNWvxi2cI6nRabHipVYCspUliWkl2pBKe6oZG3oMI1qjbenOaiJzS5RUlTDGTjK11Hg+PsyOePPxrgu+chuWxOOXcc00Utc3JoLf4X9TqYvSNKpr6Fy4upJBhyDvkHK7eIGDy+6osgd5PkPPnvUWKWlrQTlK5v8AsL18EqhH+iQb8/q7qa9KVwKicV0cWGOJVE52XNLI7kKBXaKdEak104UBrS2OhfyV+wVbSGpLYdhPyV+wU5mFSuSCBRUyGq+ulD0SE7NQzi/FUhXJ3Y+qvefPyFT8SuxDGZH9gH0j3CsDdXDSMXY5J+oeQ8qdix738i0Y2Pu7t5WLucn4AeAHdWw+TaHeZ+7sKP0if1VhgcnA3PLavXeivDOot0UjtHtN7T9wwK6WKNdC8uEFmXPfjz8PrqEwudmcY79K4J9pz9lWCKQCniwD01jf0ZnQkGNlfbvww5+VCuGXyzJqX3r3qfCtldRB1ZW3DAgjxBryNZns7h1+iSrj6S8wfbjBHtrNqce7lBq0bUHFLqpkLh1DqcqRkGpkSuUypJmojzqTRTCtUIRk1HipyldnyogIwtP2FMLVxNGgkgNIOdIlPDb0KIKaYVzT80hqEECUtPVxXZPhUCUbduwv5K/YK4qTU3DYuwufor9gq00Y5VO8BWjhqZYwKeFp2nvo0EwfSy9MkxQerH2R5n5x/V7qBN4fWa9C4J0TjkBeVTIztudbIoLMvLTudmzqz3cqzHF+AmK8a2QNuw06tyQwBByMZA338q6eOFRSGpoK9AuBa369h2EPZH0m8fd9tekAVW4fZLFGsaDAUYH3+2rS1riqQuTtnYpRXClolRrV5z8otlpmSUfwikH2p/kR9VekVlemtn6QsUasNYmUYG5AYEHsjc921Vnyi0XTM30Mv/WgPm6/+Q+w+81qlNCb7ovHaMkoMoaPSza9BVlIIYdn1TzxzG2KMqlcrUQ2ysMhw3pQormqFqzlTp28KrEGnmo3GaFgYoNOqMLXKDVkAkzSE05Vxv5VBwu662KOQgAsoJHhRoJZVdqa4qTNRYyaDIKMVJrFM0V3VVUJNYxnQn5K/YKn01gFguJOsW2NuphsbSZUe0t5XnkkhLsOsdchjoY5Oam4nwy6h9JZrm1ZIFifUvDbMtKrKrzFVOB+DjZW3Paz3VrWm+ZDc+6mTKdJ9lYS/tLhHZEubZtEl1Exbhlmvat7X0k6cE5UghcnGNzjxtcU4PdwiY9fC/VKSUHC7EStiWSLVpZwBGerLBtWSM7eJ9X+ZLPXobEKTjYZXGPABdv0fjQzjyQvKqmJmnRdSONtAYsoJbO4yDtvXi3AuLXc8VtKbi2X0i5NqESwtnZHwCuvKqMHI5E4BB8QF4Rf3rXUInjt3tpzcIky2tsnWrGkpVgypqQEjUN+W4rUmSz2yuzTIfUU/ij7BT60oh2KSlpDUILTbKZkZECoQzt2t9WDqYjH1711Rm6WJwz4A04VjsoZjvqbkuwG/marLoQI8Vs0dWZ+WntZ5aVyxz8frrxEdO5hgBkI8erJPlnzrZdPOmsQha3hlVjIuksGGyn1m5/O5DyJPhXlzXCA6iygcs5Hdj76zTin1GRXHJoT01nPev5tq5el9wfoe9CPtNAPSkPz1+sUqyg8iDWdwj7hm1GhHSq4/wDh/wBE/fSr0rn71jPub+9Wf1V2qq7EDYg8emM2fVj/AKL/AH05OmUn8Wn6YrPF67WPEUdi9xNiNdYdLNRKzKqAg4YZwNj62e7zot0Xz6LFn6J/7jXm8hJBGPjRvgHSSSDCOpeL2jUv5PiPKhKHHBSUPcbniF4IlUkZLOqAflHGfcMmrGvFBeIXizSWqxkOC5fI3wEHf4c/hRkrSZKkhZG0hpuo+NSaaTFUIZPhVvdNdE21xDB1dlw2R2lRnB0xdnGO7ds+VGIOhPFJYYwnEbcxCJ4ioSULMrwJbkyjP4QhEXBPI799VOA38MEl3NcK7xJw3hxdUGXwUC7DI8d8nGM52zQ2/wDl0WJOrsbPCgbPO5J98ae75/ltiuoA0TfJ/wAVPXk3loTOzuSYWJRpI+pkMZPqFo8KfLliq/FujN7DFILu/wCGLFI0jsJ48IWklaUkaiN9bEii3yV9N5OK21ykxVbhCf3MFBokUhCu5OQwYZ/J8a+a7mZ3YtIzO55sxLMceJO9Qh690F6KyyBorDiVrL6NKZiepm7LzRNCCGYAN2VJGM4IBq1cdG72wn4bBcXYmiHpIjRes7OmB8atRwcBtK+AyKzv/s/8W6rifVE9m4idMd2pPwin6lcfzq9S+U/9+cL/ACrz/wC3qENPAOwv5K/YKdp86ZCewv5I+wVJitKLDM12akppNGyUMNDuNEEIhAIZskHwUZ+3SPfRImgzyh3Zhuo7C/X2iPfgfzaTnntgwpHmHSro8IJdajKPjTnkuMkofr/3igihe8DHhtsds/ZXr/EbNJY2jYZVvrB7iPAivKOkHCJIJSrAYx2WyO0N99+/yrFjyXwxseSHK+XwpetHiKHlfL6qQITyUn3Uyi9MvmVfEUjSqe8fCqwtJPoNXNaSDmjfVQpEplgMn4vwpda+I+FVYrV25L/vnT0sZCcBd/DIqUiUyVpV+lj3iuDj6fxFIeFzDcpgeJIFRmxk+j3Z9ZeX10OCUy9YXzRSCSNwCO7uPiD5V6FwXj8dwMZCyd6EjfzXxFeXC1fGdO3tX76v9GIs3MR2AVgWJIGAKE4KSFyierNTMU9HDbqQR5EEfCnYrJQkC9DuHrcT3cDcpeFWMZ8tcJXPxr59lgKOUkBUqxVhtkEHDD2jevo75M/3/L/y/h39nXkHyw8I9G4tcADCysJ18+t7Tfp6x7q6YB/ye8XbhfFk60gJqMEp5Locga8n5oIR894FVIuGqOMvasMK11NbewSO8IPLu1A+6pOldl1tjY8QUesnok+O6W3GmMnzaEL/AEKC2HFW9NhuZDllmhdm7yUZSWOO84yfOoQZwO+a0u4ZiGDQTIzKNj2GGpfeAQR519FfKU4a74UQcgtdkHxBt9jXiXyt8J9G4tdKBhXfrl8CJRrOPIOXHur0K04r6TbcBcntILyJu85igMYz5lVU++oQ3nRbjqXEKEHDhQGXwOPso1XiXAnnVkaDWXwPVBOfIjwr0SO7unADOkbjOrQuoA9y9rOTzzjlTe0SVsY40ajO9NdwBknHmeVZ+OWX50kp8dJjx7uyDUymL50crn8ftfVk4FRZYPvKlq6naUaYfVOzSchj8Q43PdnkKoyQ9WGcYXRgPHjbTsdS47wM4PfuKvHiPhG/6P31RmLSMWfsr2RpGNwpJGo+08h4VTLlxuLsIuN6FdIuFi4iZMdobofBvuNFGrsVy75tBTrk8Tubdo2KMCCCQR4EUikhR+V9or1XiPAbaV9ckZyfWKkjPmcc6pcX6EwtCTbgrIN1yxIb8U55Z8a1RyWjVGSZiRJnSPxPsplvIWb/AHy0kVVkV0YgqQRlSCOR76jilKk+YxVqRey5bNgE+Y/XmiPC9pGJ7gQKE9Z2Ae84+GaIW0u4bxxmg0XTKnSCQmGMZ+cf11dPQpRDayNeQq916OY4SrayJ5I0znO+nXk+yh/HZNUa8tnI+BraX81uI+BK8bm4K2HVSB8IgFxBrDJ84kZxTMfQw5/zgt/kxk62ONLqGQNM9u7KrZikSJ5tLKTv2U8fnCq9p8njyQo/pMIlkikmjtyG1OiHc6uQ5ju7631nxe2XiaWcJkeVr+4uJSyhUQ+iSoUU/O7vj5CgV7bXMjcNW1lWGX9j5yXYAgoGTWuCrbnbu7udXEmd+TSfSZ/okRE+A3ffH669A69fpD6xXl3QyXCzY7xF9r1o+tNZMsbmzTDFuimaf5M/3/L/AMv4d/Z1nP8A2k+EfvW7AHz4HPf/ABkY/tal4Fx2SzvC8cCzdZacMhAaZIe28Z0KpYHUxAc4/EPfgUY490ia9hWO64UjxEiVM3mFcqzIpUpHnffY42cZ51rMxhvkntVv7DiPC2I1sFuIc90i4Un2ahCD5MazHBvk04pc+paSIufWmxEB54kwSPYDXrlr0uWwhaSLhEFvGFdiyTKjOI20MP3DUW1AbNjmKLN8od0GCtw5V1dThjdLp/DGRU/gs+tGV5bFk7mBqEE6b/JivE5reaWYwtHEI5Aihi+DqGGJAXBZ98HOaAcb6JwcNl4bBAZGVpb2RjIQWLG2VSdgANlHd3Uam+U2dQp/Y9TrZAALkA9vqQGw0IyuZ4QSM7yDwOAXSPpDNdXtgJbZYND3gGJllLHqGDbBQVxhTvvh12qENLDq0LyUaR2UGkchzPM/CpFAAAGwHcKSFToX2D7K4iudPJKXVlzg2Kk1GoxSlqqmAXNcPCmhq52qWA5qUGmZrhQsg5jTIpSmFO6b4PevkfEedOA3qeOjGVMvGTTAvFDHnrFO/wA5cEagO8bet9tZrj3DUmAZcBwNvxh4H763zxio2hHhTVlov2rPI24S+nI0nHduD7MGobaTtb91euvZK3rKp9wqFuFQnnEm/wCKKt26fcWjma6nk/GosRIdt3P2Gjicb4iLe0j6m3KZtlt8rGZzodWgOOs1hWaP1iACM77g0V6fcDZoE6iHOl8sEXtadJGcDc745eNZOz6W3saJCjAaMKo6tDJlVaNAcjJKhyFzuNvAU/FJSiKyS3SsJWUHFBevfpbgzJNcBzherSRYz1oI17DQxIOcHbBNE1veMQwtEYrcCKJx1rG2M0MbndRJ1uFzjZSMnT34oM3FuK5z1dxntasW7gSFoo4iXULhjpjTu2IzUdz01vlkZn0JLoMZLQqrgN+UMg+XLyO1NFkHRBc9aB4R/wDlWiw3h9v3Uz5OOHSxiZ3jZFYRhdQwTp15wDvjcb1s6xZclTY+GVxVALoxZQy3komdl02HD2XTK8WWEex7LLk93PkxHeaB9MPwN7ZRAyrbyFi+i5VS51hmReunZIsZU51KDrwPVracN6K2dzBBLPbpI/UxLqbOcKgCjY9wFWP2gcN/kcX6X31tQgy/yjcCgTh8zxuYivqpJcyjUGZWZVj1yRyliPmae7wolYWvD+q4ak07dZcwo5zc3WesVY5iRpfRGRIc9rG/Ki37QOG/yOL9L7679oHDf5HF+l99QhkuhfDYZrjiVvcSO0drJGbZWuCpyusIdUbL1hxFDuT81fCn8b4Rbw3/AA94X7cnpLSxGcysrG3wGCFmKrhAM6uSqMbVqv2gcN/kcX6X302TohY26vNDbRpIiSFXGcg6GHefAmoQswMdC+wfYKk0Ult6q/kj7KfneuSXoiCmkZKnYU3TmimVZXRN6VhUqKKXG9QBANq6p3FNUb0GwjFBzUyUiVLiomQTFcKeBSkUSDGWmGrGKYwoEISKF8X4Fb3H7rErHGNXJx7GG/u5UYakK0U66EMf+1S4UdUnEblbc84tTahj5oYMAF8sY8jRDhXRy2t944xq/jG7T/WfV92KOMN6jkFXllk1TYCCQ1FmpHFNxSgNn//Z']
    #testing base64 image
])
def test_predictAPI(client, capsys, image): 
    with capsys.disabled():
        data = image

        response = client.post('/api/predict', data=json.dumps(data), content_type="application/json")

        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"
        response_body = json.loads(response.get_data(as_text=True))
        assert response_body["result"] == "Neutral"
        assert len(response_body["probability"]) == 6

