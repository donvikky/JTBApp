var TotalEnrollments=0;
var	service_handle = "";
var	fingerpos = ["LEFT_THUMB", "LEFT_INDEX", "LEFT_MIDDLE", "LEFT_RING", "LEFT_LITTLE",
				"RIGHT_THUMB", "RIGHT_INDEX", "RIGHT_MIDDLE", "RIGHT_RING", "RIGHT_LITTLE" ];

function Restart()
{
    TotalEnrollments = 0;
    location.reload(true);
}

function captureFP( arridx ) 
{    
    CallSGIFPGetData( arridx,  SuccessFunc, ErrorFunc);
}


/* 
    This functions is called if the service sucessfully returns some data in JSON object
    Always check for ErrorCode 
    */
function SuccessFunc( arridx, fpdata )
{
    //var	imgid = fingerpos[arridx];
    //var	val  = imgid + "_INFO";
    if ( fpdata.ErrorCode == 0 )
    {
        if ( service_handle != "" && fpdata.SerHandle != service_handle )
        {
            alert("Session Timeout you will need to restart");
            Restart();
            return;
        }
        service_handle = fpdata.SerHandle;
        if ( fpdata.Result == 2 )
        {
            alert("Duplicate Finger!");
        }
        else if ( fpdata.Result == 1 )
        {
            alert("Higher or same NFIQ than earlier rejecting");
            /*document.getElementById(val).innerHTML = "Attempts = " + fpdata.Attempts + 
                " NFIQ = " + fpdata.NFIQ; */
        }
        /*
            Successful execuation gets the JSON object with all the templates  currently scanned
        */
        else if ( fpdata.Result == 0 )
        {
            if ( fpdata.BMPBase64.length > 0   )
            {
                document.getElementById(arridx).src = "data:image/bmp;base64," + fpdata.BMPBase64;
                document.getElementById(arridx).width = "120";
                document.getElementById(arridx).height = "150";

                //use jquery here to set the value of the corresponding textarea
                $('#'+arridx).parent().parent().find('textarea').text(fpdata.BMPBase64);
                //alert(fpdata.BMPBase64)
            }
            /*document.getElementById(val).innerHTML = "Attempts = " + fpdata.Attempts + 
                " NFIQ = " + fpdata.NFIQ;*/
        }
        if ( fpdata.Attempts >= 3 || fpdata.NFIQ == 1 )
        {/*
            var btnid = "BTN_" + imgid;
            document.getElementById(btnid).disabled = true;*/
        }
    }
    else 
    {
        TotalEnrollments--;
        alert("Fingerprint Capture Error Code:  " + fpdata.ErrorCode + ".\nDescription:  " + ErrorCodeToString(fpdata.ErrorCode) + ".");
    }
    //UpdateDuration();
}

function ErrorFunc( status )
{
    
    /* 	
        If you reach here, user is probabaly not running the 
        service. Redirect the user to a page where he can download the
        executable and install it. 
    */

    alert("Check if SGIBIOSRV is running; If NOT installed, then install at top of page; status = " + status + ":");
}
function CallSGIFPGetData( arridx, successCall, failCall )
{
    var	sgifpdata;
    var	uri 	= "https://localhost:8443/SGIFPEnroll";
    var	params 	= "timeout=" + "10000";
            params  += "&quality=" + "40";
            params  += "&srvhandle=" + service_handle;
            params  += "&FingerPos=" + fingerpos[arridx];

        
    var	xmlhttp = new XMLHttpRequest();
    xmlhttp.open("POST", uri, true );
    xmlhttp.onreadystatechange=function()
    {
        if (xmlhttp.readyState==4 && xmlhttp.status==200)
        {
            TotalEnrollments++;
            fpobject = JSON.parse(xmlhttp.responseText);
            ENROLL_OBJ = fpobject;
            successCall( arridx, fpobject);
        }
        else if ( xmlhttp.status == 404 )
        {
            failCall(xmlhttp.status)
        }
    }
    xmlhttp.onerror=function()
    {
        failCall(xmlhttp.status);
    }
    xmlhttp.send(params);
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

