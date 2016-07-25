$(document).ready(function(){
	var interval_code;
	var count_interval = 300;
	var top = 15;

	$("#today").click(function(){
		draw_today();

	});

	$("#current_detail").click(function(){
		draw_detail();
	});

	$("#current_detail").click();

	function sort_keys(obj){
		var domain_keys = Object.keys(obj).sort(function(a,b){return obj[a] - obj[b]}).reverse()
		return domain_keys;

	}

	function format_seconds(seconds){
		if(seconds <60){
			return seconds+" Seconds";
		}else if(seconds >=60 && seconds< 3600){
			return Math.floor(seconds/60)+" Minutes "+seconds%60+" Seconds";
		}else if(seconds > 3600){
			var hour = Math.floor(seconds/3600);
			var minute = Math.floor((seconds-hour*3600)/60);
			return hour+" Hour "+minute+" Minutes "+seconds%60+" Seconds";
		}
	}

	function timestamp_to_string(timestamp){
		return new Date(parseInt(timestamp)).toLocaleString().replace(/:\d{1,2}$/,' ').replace(/\d{4}\/\d{1,2}\/\d{1,2}/,"");
	}

	function get_detail_data(){

		var domains = JSON.parse(localStorage["domains"]);
		var domain_keys = sort_keys(domains);
		var return_data = {}
		return_data['domains'] = []
		return_data['times'] = []
		for (var i in domain_keys){
			return_data['domains'].push(domain_keys[i]);
			return_data['times'].push(domains[domain_keys[i]]);
		}
		return return_data

	}

	function get_detail_title(){
		var time = localStorage['time'];
		var time_start = time - count_interval;
		return timestamp_to_string(time_start*1000) + " 到 "+timestamp_to_string(time*1000)+" 的访问记录";

	}
	function draw_detail(){

		var data = get_detail_data();
		var title = get_detail_title();
	    $('#chart_div').highcharts({
	    	title:{
	    		text:title,
	    		style:{
	    			fontSize:"13px",
	    			fontWeight:"bold"
	    		}
	    	},
	    	credits:{
	    		text:"",
	    		href:""
	    	},
	        chart: {
	            type: 'bar'
	        },
	        xAxis: {
	            categories: data['domains']
	        },
	        legend: {
	            enabled:false
	        },
	        tooltip: {
	            formatter: function () {
	                return format_seconds(this.y);
	            }
	        },
	        series: [{
	            data: data['times'],
	            name:"domain"
	        }],
	        yAxis:{
	        	title:{
	        		text:"visiting time (Seconds)"
	        	}
	        }
	    });

	}

	function get_today_data(){		
		var domains = JSON.parse(localStorage["today_domains"]);
		var domain_keys = sort_keys(domains);
		var top_keys = domain_keys.slice(0,top);
		var other_keys = domain_keys.slice(top+1,-1);
		var total_time = 0;
		var other_time = 0;
		for (var i in domain_keys){
			total_time += domains[domain_keys[i]];
		}
		for (var i in other_keys){
			other_time += domains[other_keys[i]];
		}

		var data = [];
		var percentage = 0;
		for (var i in top_keys){
			var percentage = Math.floor(domains[top_keys[i]]/total_time*360) + percentage;
			percentage = percentage>180 ? percentage-180:percentage;
			var rotation = percentage - 90;
			data.push({"name":top_keys[i],"y":domains[top_keys[i]],"dataLabels":{"rotation":rotation}});
		}

		var percentage = Math.floor(other_time/total_time) + percentage;
		var rotation = percentage - 90;
		data.push({"name":"others","y":other_time,"dataLabels":{"rotation":rotation}});
		return data;

	}

	function draw_today(){

		var data = get_today_data();

	    $('#chart_div').highcharts({

	    	chart: {
	            plotBackgroundColor: null,
	            plotBorderWidth: null,
	            plotShadow: false
	        },
	    	title:{
	    		text:"今日 top"+top+" 访问记录",
	    		style:{
	    			fontSize:"13px",
	    			fontWeight:"bold"
	    		}
	    	},
	    	credits:{
	    		text:"",
	    		href:""
	    	},
	        tooltip: {
	            formatter: function () {
	                return this.point.name + " : " + format_seconds(this.y);
	            }
	        },
	        plotOptions: {  
                pie: {  
                    borderWidth: 0,  
                    allowPointSelect: true,  
                    cursor: 'pointer',  
                    dataLabels: {  
	                    enabled: true,
	                    distance : -65,
	                    rotation:30
                  	},  
                  	// showInLegend:true,
                  	innerSize:"50%"
                }  
            }, 
	        series: [{
	        	type:"pie",
	            data: data,
	            name:"domain"
	        }]
	    });


	}


});
