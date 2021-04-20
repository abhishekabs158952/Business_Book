from django.http import HttpResponse
from django.shortcuts import render,redirect
from mysite.models import userCredentials , originalUserCredentials ,sellerdetials, addStock,transection,transectionId, chatTable
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import logout
import datetime
from django.conf import settings
from django.core.mail import send_mail
from mysite.settings import EMAIL_HOST_USER

def fetchUserDetails(request):
  data = {'isLogin':1,'user':{'username':None},'item':None, 'shop':None, 'pincode':0, 'userType':None, 'userTypeC':None, 'userTypeS':None}
  if request.user.is_authenticated :
    username = None
    username = request.user.username
    data['user']['username'] = username 
    data['userType'] = originalUserCredentials.objects.get(userName = username).userType
    if(data['userType'] == '1'):
      data['pincode'] = userCredentials.objects.get(userName = username).address
      data['userTypeC']=1
    if(data['userType'] == '2'):
      data['pincode'] = sellerdetials.objects.get(userName = username).address
      data['userTypeS']=2
  else:
    data['isLogin']=0
  if request.POST.get('pincode'):
    data['pincode'] = int(request.POST.get('pincode'))
  return data
  
def fetchStock1(sellerId,pincode):
  item = addStock.objects.all()
  if (pincode == 0):
    return item
  else:
    itemModi = []
    for i in item:
      if i.sellerId in sellerId:
        itemModi.append(i)
    item = itemModi
  return item

def fetchShop1(pincode):
  item = None
  if(pincode == 0):
    item = sellerdetials.objects.all()
  else:
    item = sellerdetials.objects.filter(address = pincode)
  return item

def fetchShop():
  item = sellerdetials.objects.all()
  return item

def fetchStock():
  item = addStock.objects.all()
  return item

def myStock(request):
  if request.user.is_authenticated :
    data = fetchUserDetails(request)
    data['item']=fetchStock()
    data['shop']=fetchShop()
    item=fetchStock()
    itemModi=[]
    for i in item:
      if(i.sellerId==data['user']['username']):
        itemModi.append(i)
    data['item']=itemModi
    return render(request,'myStock.html',data)
  else:
    return redirect('http://127.0.0.1:8000/')
  
def search(request):
  data = fetchUserDetails(request)
  data['item'] = fetchStock()
  data['shop'] = fetchShop()
  if request.method=='POST':
    if request.POST.get('pincodeSubmit'):
      print("in pincode")
      search = int(request.POST.get('pincode'))
      shopModi=[]
      itemModi=[]
      sellerId=[]
      for i in data['shop']:
        print("shop address i :",i.address)
        if(i.address==search):
          print("i m here")
          shopModi.append(i)
          sellerId.append(i.userName)
      data['shop']=shopModi
      for i in data['item']:
        if i.sellerId in sellerId:
          itemModi.append(i)
      data['item']=itemModi
      return render(request,'b_home.html',data)
    elif request.POST.get('shopOrItemSubmit'):
      search = request.POST.get('shopOrItem')
      pincode = 0
      if request.POST.get('pincode'):
        print("in pincode")
        pincode = int(request.POST.get('pincode'))
      data['pincode'] = pincode
      print("pincode to be checked: ",pincode)
      shopModi = []
      itemModi = []
      sellerId=[]
      for i in data['shop']:
        if(i.shopName.lower().find(search.lower()) != -1):#              i.address==search):
          print("i m here")
          shopModi.append(i)
          sellerId.append(i.userName)
      data['shop']=shopModi
      shopModi = []
      sellerId=[]
      if(pincode != 0):
        for i in data['shop']:
          if(i.address==pincode):
            print("i m here")
            shopModi.append(i)
            sellerId.append(i.userName)
        data['shop']=shopModi
      for i in data['item']:
        if i.sellerId in sellerId:
          itemModi.append(i)
      data['item']=itemModi
      return render(request,'b_home.html',data)
    else:
      return redirect('http://127.0.0.1:8000/')
  return redirect('http://127.0.0.1:8000/')
  
def home(request):
  data = fetchUserDetails(request)
  data['shop'] = fetchShop1(data['pincode'])
  sellerIdStart = []
  for i in data['shop']:
    sellerIdStart.append(i.userName)
  data['item'] = fetchStock1(sellerIdStart,data['pincode'])
  if request.user.is_authenticated :
    return render(request, "b_home.html", data)
  if request.method =='POST':
    if request.POST.get('name') and request.POST.get('userName') and request.POST.get('phone') and request.POST.get('email') and request.POST.get('password1') and request.POST.get('password2') and request.POST.get('address'):
      saverecord = userCredentials()
      saverecord.name = request.POST.get('name')
      saverecord.userName = request.POST.get('userName')
      saverecord.phoneNumber = request.POST.get('phone')
      saverecord.email = request.POST.get('email')
      saverecord.address = request.POST.get('address')
      if ( request.POST.get('password1') == request.POST.get('password2')):
        saverecord.save()
        saverecorduser= originalUserCredentials()
        saverecorduser.userName = request.POST.get('userName')
        saverecorduser.password = request.POST.get('password1')
        saverecorduser.userType = request.POST.get('userType')
        saverecorduser.save()
        user = User.objects.create_user(request.POST.get('userName'), request.POST.get('email'), request.POST.get('password1'))
        user.save()
        messages.success(request,"Record saved succesfully")
        return render(request,"b_home.html", data)
      else:
        messages.error(request,"Password did not match")
        return render(request,"customer_signup.html")
    else:
      return render(request,'b_home.html', data)
  else:
    return render(request,'b_home.html', data)

def homeSeller(request):
  data=fetchUserDetails(request)
  if request.user.is_authenticated :
    data['item'] = transection.objects.all()
    filterItem=[]
    for item in data['item']:
      if(item.sellerId == data['user']['username'] and item.orderStatus == 0):
        filterItem.append(item)
    data['item']=filterItem
    return render(request, "seller_home.html", data)
  if request.method == 'POST':
    if request.POST.get('name') and request.POST.get('userName') and request.POST.get('phone') and request.POST.get('email') and request.POST.get('password1') and request.POST.get('password2') and request.POST.get('address') and request.POST.get('shopName') and request.POST.get('typeOfShop'):
      saverecords = sellerdetials()
      saverecords.name = request.POST.get('name')
      saverecords.userName = request.POST.get('userName')
      saverecords.phoneNumber = request.POST.get('phone')
      saverecords.email = request.POST.get('email')
      saverecords.address = request.POST.get('address')
      saverecords.typeOfShop = request.POST.get('typeOfShop')
      saverecords.shopName = request.POST.get('shopName')
      if ( request.POST.get('password1')== request.POST.get('password2')):
        saverecords.save()
        saverecorduser= originalUserCredentials()
        saverecorduser.userName = request.POST.get('userName')
        saverecorduser.password = request.POST.get('password1')
        saverecorduser.userType = request.POST.get('userType')
        saverecorduser.save()
        user = User.objects.create_user(request.POST.get('userName'), request.POST.get('email'), request.POST.get('password1'))
        user.save()
        messages.success(request,"Record saved succesfully")
        return render(request,"seller_home.html", data)
      else:
        messages.error(request,"Password did not match")
        return render(request,"seller_signup.html")
    else:
      return render(request,'b_home.html', data)
  else:
    return render(request,'b_home.html', data)
  
def seller_signup(request):
  return render(request,'seller_signup.html')

def customer_signup(request):
  return render(request,'customer_signup.html')

def login1(request):
  if request.method == 'POST':
    username = request.POST.get('userName')
    password = request.POST.get('password1')
    user = authenticate(request, username=username, password=password)
    if user is not None:
      login(request, user)
      data = fetchUserDetails(request)
      if request.user.is_authenticated :
        userType=1
        for p in originalUserCredentials.objects.raw('SELECT userName, userType FROM usercredentials'):
          print(p.userName,p.userType)
          if(p.userName==username):
            userType = p.userType
        if userType=='1':
          return redirect('http://127.0.0.1:8000/') #render(request,'b_home.html',data)
        else:
          return redirect('http://127.0.0.1:8000/@@') #render(request,'seller_home.html',data)
    else:
      messages.error(request," Username and Password did not match")
      return render(request,'b_home.html')
  else:
    return redirect('http://127.0.0.1:8000/')

def add_Stock(request):
  data = fetchUserDetails(request)
  if not request.user.is_authenticated :
    return render(request,"b_home.html",data)
  if request.method == 'POST':
    print("1")
    if request.POST.get('itemName') and request.POST.get('stock') and request.POST.get('cost') and request.POST.get('customerPrice') and request.POST.get('sellerPrice'):
      print("2")
      print("im elif")
      saverecords = addStock()
      saverecords.itemName = request.POST.get('itemName')
      saverecords.sellerId = data['user']['username']
      saverecords.cost = request.POST.get('cost')
      saverecords.customerPrice = request.POST.get('customerPrice')
      saverecords.sellerPrice = request.POST.get('sellerPrice')
      saverecords.itemStock = request.POST.get('stock')
      saverecords.save()
      messages.success(request,"Record saved succesfully")
      return render(request,"addStock.html",data)
    else:
      return render(request,'addStock.html',data)
  else: 
    return render(request,'addStock.html',data)

def logoutFBT(request):
  logout(request)
  return redirect('http://127.0.0.1:8000/')

def billBook(request):
  data = fetchUserDetails(request)
  items = {'isLogin':1,'n':range(2), 'user':{'username':None},'item':{'itemId':None, 'itemName':None, 'cost':None, 'sellerPrice':None, 'customerPrice':None, 'itemStock':None },'shopName':None,'length':None,'zipped':None}
  items['userTypeC']=data['userTypeC']
  items['userTypeS']=data['userTypeS']
  if request.user.is_authenticated :
    items['user']['username']=data['user']['username']
  else:
    return render(request, "b_home.html", data)
  item = addStock.objects.all()
  itemFilter=[]
  items['item']=item
  for i in items['item']:
    if(i.sellerId==data['user']['username']):
      itemFilter.append(i)
  items['item']=itemFilter
  length=len(itemFilter)
  arr=range(length)
  items['length']=arr
  shopName=None
  for p in sellerdetials.objects.raw('SELECT userName,shopName FROM sellerdetails'):
    if(p.userName==data['user']['username']):
      shopName=p.shopName
  items['shopName']=shopName
  zipped=zip(itemFilter,arr)
  items['zipped']=zipped
  return render(request, 'billBook.html',items)

def QandA(request):
  return render(request,'QandA.html')

def updateBill(billedItemList,quantity,sellerId):
  transectionVar = transection()
  transectionVar.sellerId = sellerId
  transectionVar.customerId = 'SelfBilled'
  transectionVar.dateTime = datetime.datetime.now()
  transectionVar.orderStatus = 4
  transectionVar.totalAmount = 50
  transectionVar.save()
  totalAmount=0
  for item,q in zip(billedItemList,quantity):
    print("item: ",item.itemId)
    stockItem = addStock.objects.get(itemId = ((int)(item.itemId))) # object to update
    print('stockItem: ',stockItem)
    stockItem.itemStock = stockItem.itemStock - int(q) # update name
    stockItem.save() # save object
    transectionIdVar = transectionId()
    transectionIdVar.transectionId = transectionVar.id
    transectionIdVar.itemId = int(item.itemId)
    transectionIdVar.quantity = int(q)
    transectionIdVar.price = item.customerPrice
    transectionIdVar.total = item.customerPrice * int(q)
    transectionIdVar.save()
    totalAmount+=transectionIdVar.total
  transectionVar.totalAmount = totalAmount
  transectionVar.save()
  return

def bill(request):
  if request.method=='POST':
    data = fetchUserDetails(request)
    items = {'isLogin':1,'n':range(2), 'user':{'username':None},'item':{'itemId':None, 'itemName':None, 'cost':None, 'sellerPrice':None, 'customerPrice':None, 'itemStock':None },'shopName':None,'length':None,'zipped':None,'total':0}
    if request.user.is_authenticated :
      items['user']['username']=data['user']['username']
    else:
      return redirect('http://127.0.0.1:8000/@@')
    item =addStock.objects.all()
    itemFilter=[]
    items['item']=item
    for i in items['item']:
      if(i.sellerId==data['user']['username']):
        itemFilter.append(i)
    items['item']=itemFilter
    length=len(itemFilter)
    arr=range(length)
    items['length']=arr
    shopName=None
    for p in sellerdetials.objects.raw('SELECT userName,shopName FROM sellerdetails'):
      if(p.userName==data['user']['username']):
        shopName=p.shopName
    items['shopName']=shopName
    
    billedItemList=[]
    quantity=[]
    for i,iteritem in zip(arr,itemFilter):
      j=str(i)
      if request.POST.get(j):
        billedItemList.append(iteritem)
        quantity.append(request.POST.get(j+'q'))
    totalPerPrice=[]
    total=0
    #messages.success(request,"Billed")
    flag=0
    for billedItem,q in zip(billedItemList,quantity):
      print("item: ",billedItem.itemName,", quantity: ",q)
      totalPerPrice.append(int(billedItem.customerPrice)*int(q))
      total+=int(billedItem.customerPrice)*int(q)
      if(int(q)>int(billedItem.itemStock)):
        messages.error(request,"Quantity is more than stock")
        flag=1
    zipped=zip(billedItemList,quantity,totalPerPrice)
    items['zipped']=zipped
    items['total']=total
    if(flag==0):
      updateBill(billedItemList,quantity,items['user']['username'])

    return render(request,'showBill.html',items)
  return redirect('http://127.0.0.1:8000/@@')

def updateStock(request):
  data = fetchUserDetails(request)
  items = {'isLogin':1,'n':range(2), 'user':{'username':None},'item':{'itemId':None, 'itemName':None, 'cost':None, 'sellerPrice':None, 'customerPrice':None, 'itemStock':None },'shopName':None,'length':None,'zipped':None}
  items['userTypeC']=data['userTypeC']
  items['userTypeS']=data['userTypeS']
  if request.user.is_authenticated :
    items['user']['username']=data['user']['username']
  else:
    return render(request, "b_home.html", data)
  if request.POST.get("updateStock"):
    length = int(request.POST.get("length"))
    for i in range(length):
      strI = str(i)
      valueQ, valueCP, valueSP, valueC, valueRemove = strI+'q', strI+'cp', strI+'sp', strI+'c', strI+'rm' #value = for the quantity
      itemIdRecived = int(request.POST.get(strI + 'id'))
      if request.POST.get(valueQ):
        quantityToBeDelete = int(request.POST.get(valueQ))
        addStock.objects.filter(itemId = itemIdRecived).update(itemStock = addStock.objects.get(itemId = itemIdRecived).itemStock + quantityToBeDelete)
      if request.POST.get(valueCP):
        itemCustomerPrice = int(request.POST.get(valueCP))
        addStock.objects.filter(itemId = itemIdRecived).update(customerPrice = itemCustomerPrice)
      if request.POST.get(valueSP):
        itemSellerPrice = int(request.POST.get(valueSP))
        addStock.objects.filter(itemId = itemIdRecived).update(sellerPrice = itemSellerPrice)
      if request.POST.get(valueC):
        itemCost = int(request.POST.get(valueC))
        addStock.objects.filter(itemId = itemIdRecived).update(cost = itemCost)
    return redirect('/updateStock')
  elif request.POST.get("removeItem"):
    itemId = int(request.POST.get("removeItem"))
    addStock.objects.get(itemId = itemId).delete()
    return redirect('/updateStock')
  else:
    item = addStock.objects.all()
    itemFilter=[]
    items['item']=item
    for i in items['item']:
      if(i.sellerId==data['user']['username']):
        itemFilter.append(i)
    items['item']=itemFilter
    length=len(itemFilter)
    arr=range(length)
    items['length']=arr
    items['noOfItem']=length
    shopName=None
    for p in sellerdetials.objects.raw('SELECT userName,shopName FROM sellerdetails'):
      if(p.userName==data['user']['username']):
        shopName=p.shopName
    items['shopName']=shopName
    zipped=zip(itemFilter,arr)
    items['zipped']=zipped
    return render(request, 'updateStock.html',items)

def shopDetails(request):
  if request.method=='POST':
    if request.POST.get('shopUser'):
      data = fetchUserDetails(request)
      items = {'isLogin':1,'n':range(2), 'user':{'username':None},'item':{'itemId':None, 'itemName':None, 'cost':None, 'sellerPrice':None, 'customerPrice':None, 'itemStock':None },'shopName':None,'length2':None,'zipped':None}
      items['sellerId'] = request.POST.get('shopUser')
      if request.user.is_authenticated :
        items['user']['username']=data['user']['username']
      else:
        items['isLogin']=0
      items['shopName'] = request.POST.get('shopUser')
      item = addStock.objects.all()
      itemFilter=[]
      items['item']=item
      for i in items['item']:
        if(i.sellerId==request.POST.get('shopUser')):
          itemFilter.append(i)
      items['item']=itemFilter
      length=len(itemFilter)
      items['length2']=length
      arr=range(length)
      items['length']=arr
      shopName=None
      for p in sellerdetials.objects.raw('SELECT userName,shopName FROM sellerdetails'):
        if(p.userName==request.POST.get('shopUser')):
          shopName=p.shopName
      items['shopName'] = shopName #request.POST.get('shopUser')
      zipped=zip(itemFilter,arr)
      items['zipped']=zipped
      return render(request, 'shopDetails.html',items)
    else:#if request.POST.get('buyNow'):
      data = fetchUserDetails(request)
      if data['isLogin']==0:
        return redirect('http://127.0.0.1:8000/')
      saverecord = transection()
      saverecord.sellerId = request.POST.get('sellerId')
      saverecord.customerId = data['user']['username']
      saverecord.dateTime = datetime.datetime.now()
      saverecord.totalAmount = 50
      if request.POST.get('buyNow'):
        saverecord.orderStatus = 0
      else: 
        saverecord.orderStatus = 3
      saverecord.save()
      totalAmount=0
      #length1=int(request.POST.get('length'))
      print("value of length: ",int(request.POST.get('length2')))
      for i in range(int(request.POST.get('length2'))):
        print(i)
        j=str(i)
        if request.POST.get(j):
          transectionIdVar = transectionId()
          transectionIdVar.itemId = request.POST.get(j)
          transectionIdVar.transectionId = saverecord.id
          transectionIdVar.quantity = request.POST.get(j+'q')
          transectionIdVar.price = request.POST.get(j+'p')
          transectionIdVar.total = int(request.POST.get(j+'q'))*int(request.POST.get(j+'p'))
          totalAmount += transectionIdVar.total
          transectionIdVar.save()
      saverecord.totalAmount=totalAmount
      saverecord.save()
      return redirect('http://127.0.0.1:8000/')
    '''elif request.POST.get("addToCart"):
      return redirect('http://127.0.0.1:8000/')'''
  return redirect('http://127.0.0.1:8000/')

def itemDetails(request):
  data = fetchUserDetails(request)
  if(data['isLogin'] == 0):
    return redirect('http://127.0.0.1:8000/')
  if request.method=='POST':
    item = None
    if request.POST.get('shopUser'):
      item = addStock.objects.filter(itemName = request.POST.get('shopUser'))
    sellerIds = []
    for i in item:
      sellerIds.append(i.sellerId)
    shop = sellerdetials.objects.filter(userName__in = sellerIds)
    data['shop'] = shop
    '''items = {'isLogin':1,'n':range(2), 'user':{'username':None},'item':{'itemId':None, 'itemName':None, 'cost':None, 'sellerPrice':None, 'customerPrice':None, 'itemStock':None },'shopName':None,'length':None,'zipped':None}
    if request.user.is_authenticated :
      items['user']['username']=data['user']['username']
    else:
      items['isLogin']=0
    item = addStock.objects.all()
    itemFilter=[]
    items['item']=item
    for i in items['item']:
      if(i.itemName==request.POST.get('shopUser')):
        itemFilter.append(i)
    items['item']=itemFilter
    length=len(itemFilter)
    arr=range(length)
    items['length']=arr
    shopName=None
    for p in sellerdetials.objects.raw('SELECT userName,shopName FROM sellerdetails'):
      if(p.userName==data['user']['username']):
        shopName=p.shopName
    items['shopName']=shopName
    zipped=zip(itemFilter,arr)
    items['zipped']=zipped'''
    return render(request, 'itemToShop.html',data)
  return redirect('http://127.0.0.1:8000/')

def showDetails(request):
  data=fetchUserDetails(request)
  if request.method=='POST':
    if request.POST.get('showDetails') :
      item = transectionId.objects.all()
      transId = int(request.POST.get('showDetails'))
      itemFilter=[]
      totalAmount = 0
      total = []
      for i in item:
        if(i.transectionId == transId):
          itemFilter.append(i)
          total.append(i.quantity * i.price)
          totalAmount += i.quantity * i.price
      data['item'] = zip(itemFilter,total)
      data['totalAmount'] = totalAmount
      return render(request,'showDetails.html',data)

    if request.POST.get('orderNow') :
      transId = int(request.POST.get('orderNow'))
      transection.objects.filter(id = transId).update(orderStatus = 0)
      return redirect('cart')

    if request.POST.get('removeFromCart') :
      transId = int(request.POST.get('removeFromCart'))
      transection.objects.filter(id = transId).delete()
      return redirect('cart')
    
    if request.POST.get('delivered') :
      transId = int(request.POST.get('delivered'))
      transection.objects.filter(id = transId).update(orderStatus = 4)
      return redirect('allTransection')

def transectionValidity(request):
  if request.method=="POST":
    if request.POST.get("validity"):
      id=str(request.POST.get("id"))
      if request.POST.get("validity") == "accept":
        transectionIdVal = transectionId.objects.filter(transectionId=id)
        processFlag=1
        for tran in transectionIdVal:
          if addStock.objects.get(itemId = tran.itemId).itemStock < tran.quantity:
            processFlag=0
        if processFlag == 1:
          for tran in transectionIdVal:
            addStock.objects.filter(itemId = tran.itemId).update(itemStock = addStock.objects.get(itemId = tran.itemId).itemStock - tran.quantity)
          transection.objects.filter(id=id).update(orderStatus = 1)
      elif request.POST.get("validity") == "reject":
        transection.objects.filter(id=id).update(orderStatus = 2)
  return redirect("/@@")

def allTransection(request):
  data = fetchUserDetails(request)
  data['order']={'pending':None, 'confirm':None, 'rejected':None }
  data['order']['pending'] = transection.objects.filter(sellerId = data['user']['username']).filter(orderStatus = 0)
  data['order']['confirm'] = transection.objects.filter(sellerId = data['user']['username']).filter(orderStatus = 1)
  data['order']['rejected'] = transection.objects.filter(sellerId = data['user']['username']).filter(orderStatus = 2)
  data['order']['delivered'] = transection.objects.filter(sellerId = data['user']['username']).filter(orderStatus = 4)
  return render(request, 'sellerTransection.html', data)
  
def myOrder(request):
  data = fetchUserDetails(request)
  data['order']={'pending':None, 'confirm':None, 'rejected':None }
  data['order']['pending'] = transection.objects.filter(customerId = data['user']['username']).filter(orderStatus = 0)
  data['order']['confirm'] = transection.objects.filter(customerId = data['user']['username']).filter(orderStatus = 1)
  data['order']['rejected'] = transection.objects.filter(customerId = data['user']['username']).filter(orderStatus = 2)
  data['order']['delivered'] = transection.objects.filter(customerId = data['user']['username']).filter(orderStatus = 4)
  return render(request, 'customerTransection.html', data)

def cart(request):
  data=fetchUserDetails(request)
  data['order']={'cart':None}
  data['order']['cart']=transection.objects.filter(customerId = data['user']['username']).filter(orderStatus = 3)
  return render(request, 'cart.html',data)

def resetPassword(request):
  pass

def chat(request):
  data = fetchUserDetails(request)
  if(data['isLogin']):
    if request.POST.get('chat'):
      transecId = int(request.POST.get('chat'))
      chatDetails = transection.objects.get(id = transecId)
      messages = chatTable.objects.filter(transectionId = transecId)#.order_by('dateTime')
      data['chatMessages'] = messages
      data['transecId'] = transecId
      data['reciver'] = chatDetails.sellerId
      if data['reciver'] == data['user']['username']:
        data['reciver'] = chatDetails.customerId
      return render(request,'chatPage.html',data)
    elif request.POST.get('sendMessage') and request.POST.get('inputMessage'):
      messagesToSave = request.POST.get('inputMessage')
      transecId = int(request.POST.get('transecId'))
      chatDetails = transection.objects.get(id = transecId)
      saveMessage = chatTable()
      saveMessage.customerId, saveMessage.sellerId, saveMessage.transectionId, saveMessage.sender, saveMessage.dateTime, saveMessage.message = chatDetails.customerId, chatDetails.sellerId, transecId, data['user']['username'], datetime.datetime.now(), messagesToSave 
      saveMessage.save()
      messages = chatTable.objects.filter(transectionId = transecId)#.order_by('dateTime')
      data['chatMessages'] = messages
      data['transecId'] = transecId
      data['reciver'] = chatDetails.sellerId
      if data['reciver'] == data['user']['username']:
        data['reciver'] = chatDetails.customerId
      return render(request,'chatPage.html',data)
    return redirect('/')
  else:
    return redirect('/')

def myAccount(request):
  data = fetchUserDetails(request)
  if request.method == 'POST':
    if request.POST.get('nameSubmit') and request.POST.get('name'):
      if data['userType'] == '1':
        userCredentials.objects.filter(userName = data['user']['username']).update(name = request.POST.get('name'))
      elif data['userType'] == '2':
        sellerdetials.objects.filter(userName = data['user']['username']).update(name = request.POST.get('name'))
    if request.POST.get('phoneSubmit') and request.POST.get('phone'):
      if data['userType'] == '1':
        userCredentials.objects.filter(userName = data['user']['username']).update(phoneNumber = request.POST.get('phone'))
      elif data['userType'] == '2':
        sellerdetials.objects.filter(userName = data['user']['username']).update(phoneNumber = request.POST.get('phone'))
    if request.POST.get('emailSubmit') and request.POST.get('email'):
      if data['userType'] == '1':
        userCredentials.objects.filter(userName = data['user']['username']).update(email = request.POST.get('email'))
      elif data['userType'] == '2':
        sellerdetials.objects.filter(userName = data['user']['username']).update(email = request.POST.get('email'))
      User.objects.filter(username = data['user']['username']).update(email = request.POST.get('email'))
    if request.POST.get('passwordSubmit'):
      if( request.POST.get('oldPassword') == originalUserCredentials.objects.get(userName = data['user']['username']).password and request.POST.get('newPassword')):
        originalUserCredentials.objects.filter(userName = data['user']['username']).update(password = request.POST.get('newPassword'))
        u = User.objects.get(username = data['user']['username'])
        u.set_password(request.POST.get('newPassword'))
        u.save()
    if request.POST.get('uploadPhoto'):
      print("submit")
      if request.POST.get('uploadPic'):
        print("hey")
        print("image:" ,request.POST.get('uploadPic'))
  
  data['userDetails'] = None
  if (data['userType'] == '1'):
    data['userDetails'] = userCredentials.objects.get(userName = data['user']['username'])
  elif (data['userType'] == '2'):
    data['userDetails'] = sellerdetials.objects.get(userName = data['user']['username'])
  return render(request, 'myAccount.html',data)
