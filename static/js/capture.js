function captureFP() {
    CallSGIFPGetData(SuccessFunc, ErrorFunc);    
}

/* 
    This functions is called if the service sucessfully returns some data in JSON object
 */
function SuccessFunc(result) {
    if (result.ErrorCode == 0) {
        /* 	Display BMP data in image tag
            BMP data is in base 64 format 
        */
        if (result != null && result.BMPBase64.length > 0) {
            document.getElementById("f1").src = "data:image/bmp;base64," + result.BMPBase64;
        }
        
    }
    else {
        alert("Fingerprint Capture Error Code:  " + result.ErrorCode + ".\nDescription:  " + ErrorCodeToString(result.ErrorCode) + ".");
    }
}


function ErrorFunc(status) {

    /* 	
        If you reach here, user is probabaly not running the 
        service. Redirect the user to a page where he can download the
        executable and install it. 
    */
    alert("Check if SGIBIOSRV is running; Status = " + status + ":");

}


function CallSGIFPGetData(successCall, failCall) {
    // 8.16.2017 - At this time, only SSL client will be supported.
    var uri = "https://localhost:8443/SGIFPCapture";

    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            fpobject = JSON.parse(xmlhttp.responseText);
            successCall(fpobject);
        }
        else if (xmlhttp.status == 404) {
            failCall(xmlhttp.status)
        }
    }
    var params = "Timeout=" + "10000";
    params += "&Quality=" + "50";
    params += "&licstr=" + encodeURIComponent(secugen_lic);
    params += "&templateFormat=" + "ISO";
    console.log
    xmlhttp.open("POST", uri, true);
    xmlhttp.send(params);

    xmlhttp.onerror = function () {
        failCall(xmlhttp.statusText);
    }
}


    // nice global area, so that only 1 location, contains this information
    //    var secugen_lic = "hE/78I5oOUJnm5fa5zDDRrEJb5tdqU71AVe+/Jc2RK0=";   // webapi.secugen.com
    var secugen_lic = "";

    function ErrorCodeToString(ErrorCode) {
        var Description;
        switch (ErrorCode) {
            // 0 - 999 - Comes from SgFplib.h
            // 1,000 - 9,999 - SGIBioSrv errors 
            // 10,000 - 99,999 license errors
            case 51:
                Description = "System file load failure";
                break;
            case 52:
                Description = "Sensor chip initialization failed";
                break;
            case 53:
                Description = "Device not found";
                break;
            case 54:
                Description = "Fingerprint image capture timeout";
                break;
            case 55:
                Description = "No device available";
                break;
            case 56:
                Description = "Driver load failed";
                break;
            case 57:
                Description = "Wrong Image";
                break;
            case 58:
                Description = "Lack of bandwidth";
                break;
            case 59:
                Description = "Device Busy";
                break;
            case 60:
                Description = "Cannot get serial number of the device";
                break;
            case 61:
                Description = "Unsupported device";
                break;
            case 63:
                Description = "SgiBioSrv didn't start; Try image capture again";
                break;
            default:
                Description = "Unknown error code or Update code to reflect latest result";
                break;
        }
        return Description;
    }


