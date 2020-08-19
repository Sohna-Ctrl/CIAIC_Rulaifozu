//启动时方法
		window.onload=function(){
		var oDiv = document.getElementById('banner');
		var oUl = oDiv.getElementsByTagName('ul')[0];
		var Li = oUl.getElementsByTagName('li');
		oUl.innerHTML = oUl.innerHTML+oUl.innerHTML;
		oUl.style.width = Li[0].offsetWidth*Li.length+'px';//ul的宽度等于每个li的宽度乘以所有li的长度

		var speed = 2
		function move(){

		if(oUl.offsetLeft<-oUl.offsetWidth/speed){

		oUl.style.left = '0'

		}

		//如果右边横向滚动的距离大于0 就让他的位置回到一半

		if(oUl.offsetLeft>0){

		oUl.style.left = -oUl.offsetWidth/speed+'px';

		}
		//oUl.style.left = oUl.offsetLeft+speed+'px';//进行右横向滚动
		oUl.style.left = oUl.offsetLeft-speed+'px';//进行左横向滚动

		}

		//调用方法
		var timer = setInterval(move,4)//速度

		//鼠标悬停时暂停
		oDiv.onmouseover=function(){

		clearInterval(timer);

		}

		//鼠标离开之后恢复
		oDiv.onmouseout=function(){

		timer = setInterval(move,4)

		}

		}