# 자유로운 후원 플랫폼 WhoWant
### 2021 멋쟁이 사자처럼 코딩 단체에서 주최한 해커톤 대회에 제출한 웹입니다.
### World Vision, 사랑의 열매 같은 후원 플랫폼과의 차별점은 후원이 플랫폼을 거치지 않고 1대1로 피후원인에게 후원된다는 점입니다! (투명성)
![qq](https://user-images.githubusercontent.com/58176152/130022753-9caa1ee0-7d84-4f56-a9b4-616c71eaaf85.png)
![qq1](https://user-images.githubusercontent.com/58176152/130023027-b5e3360c-78cd-479d-9484-492c0f165e22.png)
![qq2](https://user-images.githubusercontent.com/58176152/130023036-a918dcce-51b8-4263-909f-778fb88b8df6.png)
#### 웹의 메인 화면입니다. 모든 기능은 로그인 후 이용가능합니다.
#### 회원가입을 마치고나면 아래의 alert창 이후 바로 아래 마이페이지 화면에 도착합니다!
![alert1](https://user-images.githubusercontent.com/58176152/130024388-7698533e-c12f-4346-8d55-c7f7dc772971.png)
### 문의하기, FAQ를 제외한 모든 기능 역시 이메일 인증 절차를 거친 뒤 이용할 수 있습니다.
### 이메일 인증을 클릭하면 마찬가지로 alert창이 뜨고 회원가입했을때의 이메일에 메일을 발송합니다.
![이멜](https://user-images.githubusercontent.com/58176152/130024085-e56febe7-6eeb-4786-8479-bc95d2eab3d2.png)
![emailverifing](https://user-images.githubusercontent.com/58176152/130024962-43dcf125-c11f-471a-8b16-b88051077236.png)
### 인증하기를 클릭하면 User DB의 Boolean Field인 active가 활성화되며 템플릿에 성공적으로 접근할 수 있습니다.
## 피후원자는 메인페이지의 [인증] 기능을 통해 기초수급자 서류의 성명과 일치하는지에 대한 인증을 해야합니다
![피후원](https://user-images.githubusercontent.com/58176152/130026015-cbe46921-1d6b-4e42-a5b4-f7d67c42344e.png)
## 샘플 서류입니다. 해당 사진을 업로드하면 홍길동으로 가입된 현재 아이디는 피후원인으로서 글을 등록할 수 있게됩니다.
## 인증 과정은 Google Vision API를 통해 텍스트를 검출하여 진행합니다.
![vr](https://user-images.githubusercontent.com/58176152/130026100-6137ee56-7ba8-45eb-a55b-639761fe03e1.jpg)
# 해당 views.py입니다.

    '''
    def verify(request):
    if request.method=='POST':
        img = request.FILES.get('image')
        if img:
            img = img.read()
        else:
            msg = "fail"
            return render(request, 'index.html', {'msg':msg})
        user = CustomUser.objects.get(email=request.user)
        real_user = UserInfo.objects.get(user_email=request.user.email)
        msg = ""
        if ggoo(img,real_user.user_name):
            real_user.qua = 'yes'
            real_user.save()
            msg = "success"
        else:
            msg = "fail"
    return render(request, 'index.html', {'msg':msg})
    '''
