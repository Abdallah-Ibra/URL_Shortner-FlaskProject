function request(url,b,method,data,c){ 
   request = new XMLHttpRequest;
   request.open(method||'get',url);
   request.onload=b;
   request.send(data||null)
  
   result = document.getElementById("result");
   result.value = 'انتظر رجاء...'
   }
  
  function callback(e){
        short_link = document.getElementById("result");
        short_link.value = window.location.host + this.response 
  }
  
  function change() {
  url = document.getElementById("input").value;
  request('shorten?link=' + url, callback, 'get')
  }
  
  // الدّالة المسؤولة عن نسخ الرّابِط المُختصر إلى لوحة مفاتيح المُستخدم
  function copy() {
      result = document.getElementById("result");
      msg = document.getElementById("msg");
      result.select();
      try {
          var copy = document.execCommand('copy');
          if(copy) msg.innerHTML = 'تم نسخ الرابط بنجاح!';
          else msg.innerHTML = 'هناك خطأ ما! أعد المُحاولة رجاء';
      }
      catch(err) {
          msg.innerHTML = 'المُتصفّح لا يدعم هذه العمليّة';
      }
  }