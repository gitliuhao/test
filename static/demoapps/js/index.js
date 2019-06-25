function response_500_alert(res) {
    var error = res.responseText.slice(0, 100);
    console.log(error)
    if (error.search("ConnectionError") != -1){
      alert("JenkinsServer没有启动")
    }else {
      alert(error)
    }
  }