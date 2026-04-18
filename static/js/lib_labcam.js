/**
 * @license
 * Author: Umi-Reco
 * License: MIT (see LICENSE file for details)
 */

const url_host = "http://127.0.0.1:5500";

function func_memory_color(var_mem){
    var mem_status_colors = "#b36200"
    if (var_mem > 80){
        mem_status_colors = "#006400";
    };
    if (var_mem < 20){
        mem_status_colors = "#ff0000";
    }
    return mem_status_colors;
};

function func_api_get_model_list(){
    const xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
        json_sys_config = JSON.parse(this.responseText);
        //Do necessary action
    };
    xhttp.open("GET", url_host + "/api/model_list");
    xhttp.setRequestHeader("Accept", "application/json");
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.send();
}

function func_api_get_camera_params(){
    const xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
        json_sys_config = JSON.parse(this.responseText);
        //Do necessary action
    };
    xhttp.open("GET", url_host + "/api/camera_params");
    xhttp.setRequestHeader("Accept", "application/json");
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.send();    
}

function func_api_get_process_status(){
       const xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
        json_sys_config = JSON.parse(this.responseText);
        //Do necessary action
    };
    xhttp.open("GET", url_host + "/api/process_status");
    xhttp.setRequestHeader("Accept", "application/json");
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.send(); 
}


//function to update the interface 
function func_api_get_system_status() {
    const xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
        json_sys_config = JSON.parse(this.responseText);
        func_update_gui(json_sys_config);
    };
    xhttp.open("GET", url_host + "/api/system_status");
    xhttp.setRequestHeader("Accept", "application/json");
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.send();
};

function func_api_get_control_status() {
    const xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
        json_sys_config = JSON.parse(this.responseText);
        func_update_controls(json_sys_config);
    };
    xhttp.open("GET", url_host + "/api/system_status");
    xhttp.setRequestHeader("Accept", "application/json");
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.send();
};

function func_update_gui(json_sys_config){
    document.getElementById("div_sys_memory").innerHTML   = '<div class="name">Memory</div>' + json_sys_config["memory"];
    document.getElementById("div_sys_memory").style.color = func_memory_color(json_sys_config["memory"]);
    document.getElementById("div_sys_datetime").innerHTML = '<div class="name">Date</div>'  + json_sys_config["datetime"];
    document.getElementById("div_dir_id").innerHTML       = '<div class="name">Model</div>'  + json_sys_config["model"];  
    document.getElementById("data_status").value          = json_sys_config["status"];  
};

function func_update_controls(json_sys_config){
    document.getElementById("data_gain").value     = json_sys_config["gain"];
    document.getElementById("data_exposure").value = json_sys_config["exposure"];
};

function func_update_models(json_sys_config){
    list_model = json_sys_config["models"]

    list_model.forEach(item => {
    const div_model_dropdown = document.getElementById("div_model_dropdown");
        let opt = document.createElement("option"); 
        opt.value = item.toLowerCase();            
        opt.textContent = item;       
        opt.label = item;             
        div_model_dropdown.appendChild(opt);                  
    });

    div_model_dropdown.addEventListener('change', (event) => {
        func_api_set_models(); 
    });
};

//function to send json to server
function func_post_json() {
    json_post_data = {
        "gain":document.getElementById("data_gain").value ,
        "exposure":document.getElementById("data_exposure").value,
        "model":document.getElementById("div_model_dropdown").value
    }
    return json_post_data
};

function func_send_data() {

    const xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
        json_sys_config = JSON.parse(this.responseText);
        func_update_gui(json_sys_config);
        func_req_update_gui();
    };

    data = func_post_json();
    xhttp.open("POST", url_host + "/api/json_test");
    xhttp.setRequestHeader("Accept", "application/json");
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.send(JSON.stringify(data));
};

//functions for deployment
function func_api_set_models() {
    const xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
        json_sys_config = JSON.parse(this.responseText);
    };
    data = func_post_json();
    xhttp.open("POST", url_host + "/api/set_model");
    xhttp.setRequestHeader("Accept", "application/json");
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.send(JSON.stringify(data));
};


//functions for deployment
function func_api_models() {
    const xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
        json_sys_config = JSON.parse(this.responseText);
        console.log(json_sys_config);
        func_update_models(json_sys_config)
    };
    data = func_post_json();
    xhttp.open("POST", url_host + "/api/get_models");
    xhttp.setRequestHeader("Accept", "application/json");
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.send(JSON.stringify(data));
};


//functions for camera

function func_api_ai_stop() {
    const xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
        json_sys_config = JSON.parse(this.responseText);
        func_show_sys_update(json_sys_config);
        func_req_update();
    };
    xhttp.open("GET", url_host + "/api/stop_ai");
    xhttp.setRequestHeader("Accept", "application/json");
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.send();
};

function func_api_ai_start() {
    const xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
        json_sys_config = JSON.parse(this.responseText);
        func_show_sys_update(json_sys_config);
        func_req_update();
    };
    xhttp.open("GET", url_host + "/api/start_ai");
    xhttp.setRequestHeader("Accept", "application/json");
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.send();
};

function func_save_camera() {
    const xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
        json_sys_config = JSON.parse(this.responseText);
        func_update_gui(json_sys_config);
    };
    data = func_post_json();
    xhttp.open("POST", url_host + "/api/save_camera");
    xhttp.setRequestHeader("Accept", "application/json");
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.send(JSON.stringify(data));
};