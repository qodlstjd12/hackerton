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
## 인증 메일
![emailverifing](https://user-images.githubusercontent.com/58176152/130024962-43dcf125-c11f-471a-8b16-b88051077236.png)
### 인증하기를 클릭하면 User DB의 Boolean Field인 active가 활성화되며 템플릿에 성공적으로 접근할 수 있습니다.
## 피후원자는 메인페이지의 [인증] 기능을 통해 기초수급자 서류의 성명과 일치하는지에 대한 인증을 해야합니다
![피후원](https://user-images.githubusercontent.com/58176152/130026015-cbe46921-1d6b-4e42-a5b4-f7d67c42344e.png)
## 샘플 서류입니다. 해당 사진을 업로드하면 홍길동으로 가입된 현재 아이디는 피후원인으로서 글을 등록할 수 있게됩니다.
![vr](https://user-images.githubusercontent.com/58176152/130026100-6137ee56-7ba8-45eb-a55b-639761fe03e1.jpg)
## 인증 과정은 Google Vision API를 통해 텍스트를 검출하여 진행합니다.
# 해당 views.py입니다.
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

### 피후원자 인증 후 피후원자의 마이페이지
![피마페](https://user-images.githubusercontent.com/58176152/130031605-b56ed171-b63b-4377-a1b2-84b06d4fd09e.png)

## 피후원자는 후원글을 등록하여 후원을 기다립니다.
![helpwrite](https://user-images.githubusercontent.com/58176152/130031822-0e186c32-d572-42e8-ba37-800dd7502863.png)
## 글을 등록했습니다.
![qq4](https://user-images.githubusercontent.com/58176152/130032373-155e59e9-9ee6-4b74-a8cc-761d777a0493.png)

## 그럼 이제 후원자의 입장에서 보겠습니다!
### 후원을 하기 위해 30000원을 충전했습니다. 충전은 숫자를 적고 충전하기를 누르면 바로 cash가 쌓이는 방식으로 구현했습니다.
![qq5](https://user-images.githubusercontent.com/58176152/130032618-2f32d0bb-850e-4196-8c29-3289c9fbb803.png)

![image](https://user-images.githubusercontent.com/58176152/130033167-d42a4075-b394-40bf-b976-22341ae6071d.png)
## 만원을 후원한 후, 후원자의 마이페이지와 피후원자의 마이페이지, 그리고 근황 기능, 아이디 비밀번호 찾기 기능을 보여드리고 마치겠습니다!

## 후원자의 마이페이지
![image](https://user-images.githubusercontent.com/58176152/130033370-dd74300e-c3f1-4699-8bf5-3049b3ced15c.png)
### 마음의 온도는 1000원 후원당 0.1도씩 올라가도록 했습니다.
### 그리고 자신이 후원했던 사람들의 근황을 볼 수 있습니다.

## 피후원자의 마이페이지
![image](https://user-images.githubusercontent.com/58176152/130033746-bec8e7fb-a972-4817-a419-d0243b8d3d5a.png)
### 후원받을때마다 우측의 거래내역이 쌓이게 됩니다. 누가 후원했는지 알 수 있습니다.
### 후원 게시글은 자신이 올렸던 후원글이 자동으로 등록됩니다.

# 후원을 받았으면 그 후원금을 어떤 곳에 썼는지 피후원자가 직접 글을 쓸 수 있습니다.
![image](https://user-images.githubusercontent.com/58176152/130034382-25747b40-bb56-4654-b215-2ea25e13753b.png)
## 중요한 점은 영수증을 등록할 때 개인정보 (전화번호, 휴대폰 전화번호, 이름) 등이 다수 발견된다면 
![image](https://user-images.githubusercontent.com/58176152/130034813-b8bc9a66-1b0e-4007-871a-3bc0dfe25a11.png)
## 그렇지 않은 영수증은 아래와 같이 글이 등록됩니다.
![image](https://user-images.githubusercontent.com/58176152/130035029-82f722eb-a936-4365-8dc6-54ab0d39f61c.png)

## Google Vision API를 통해 텍스트 검출하기 전, 정규표현식을 사용하여 걸렀습니다.
![image](https://user-images.githubusercontent.com/58176152/130035427-1a79da6d-823e-4b02-8e0d-6928ef010ed7.png)

# 아이디 찾기 / 비밀번호 찾기
### 두 기능 모두 한 HTML에서 추가적인 HTML View를 띄워야했기에 AJAX 비동기 통신이 요구되었습니다.
## ID 찾기
## 절차 1
![image](https://user-images.githubusercontent.com/58176152/130037945-4454f7b7-04c9-4ca3-a25e-42bc66122f03.png)
## 절차 2
![image](https://user-images.githubusercontent.com/58176152/130037957-9e8b0d1a-fb56-4aa6-a2ca-624ae59a0a0b.png)

## PW 찾기
## 절차 1
![image](https://user-images.githubusercontent.com/58176152/130038011-b5751db0-ac2d-4c28-9704-55349d6fa8f3.png)
## 절차 2
![image](https://user-images.githubusercontent.com/58176152/130038246-ee1cf92d-0550-4ff7-b796-12311cee4827.png)
## 절차 3
![image](https://user-images.githubusercontent.com/58176152/130038126-ca60587e-a49e-4b32-9729-744a79451c44.png)
## 절차 4
![image](https://user-images.githubusercontent.com/58176152/130038137-2c1f3dab-094c-4736-a779-fd8a42f0defb.png)
## AJAX 요청은 프론트에서 처리했습니다.

    $('.btn').click(function () {
        $.ajax({
            type: "POST",
            url: "find/",
            dataType: "json",
            data: {
                'email': $("#pw_form_email").val(),
                'csrfmiddlewaretoken': '{{csrf_token}}',
            },
            success: function (response) {
                alert('인증 메일을 발송했습니다.');
                $('.authBox').css('display', 'flex');
            },
            error: function () {
                alert('입력하신 정보를 확인해주세요.')
            },
        });
    });

    $('.authBtn').click(function () {
        $.ajax({
            type: "POST",
            url: "auth/",
            dataType: "json",
            data: {
                'email': $('#pw_form_email').val(),
                'input_auth_num': $('.authInput').val(),
                'csrfmiddlewaretoken': '{{csrf_token}}',
            },
            success: function (response) {
                window.location.href = "{% url 'user_info:recovery_pw_reset' %}";
            },
            error: function () {
                if ($('#input_auth_num').val() == "") {
                    alert('회원님의 이메일로 전송된 인증번호를 입력해주세요.');
                } else {
                    alert('인증번호가 일치하지 않습니다.');
                }
            },
        });
    })

# 이상으로 WhoWant Readme 마치도록 하겠습니다!
