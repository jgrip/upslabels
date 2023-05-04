import base64
import tempfile

from flask import Flask, request
from sh import lpr

PRINTER_NAME = "Zebra"

app = Flask(__name__)

@app.route("/listPrinters")
def list_printers():
    return """
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html;charset=UTF-8">
    <script>
        function requestPcl() {
            var pclType = document.getElementById("thermalPrinterType").value;
            var printer = document.getElementById("thermalPrinterName").value;
            if (pclType) {
                 var message = {};
                 message.requestType = "request";
                 message.labelType = pclType;
                 message.printer = printer;
                 message.windowName = window.name;
                 message.version = "3.1";
                 window.opener.postMessage(message, "https://www.ups.com/*");
            }
        }
        function waitForButtonClick() {
            var message = {};
            message.requestType = "wait";
            window.opener.postMessage(message, "https://www.ups.com/*");
        }
        function selectPrinter() {
            var selectedPrinter = document.getElementById("thermalPrinters");
            var printerType = selectedPrinter.value;
            var printerName = selectedPrinter.options[selectedPrinter.selectedIndex].innerHTML;
            document.getElementById("thermalPrinterType").value=printerType;
            document.getElementById("thermalPrinterName").value=printerName;
            console.log("thermalPrinterName selected: "+ printerName);
            requestPcl();
        }
        function receiveMessage(event) {
            var printRequest = new XMLHttpRequest();
            var printerName = document.getElementById("thermalPrinterName").value;
            console.log("thermalPrinterName requested: "+ printerName);
            var query = "printerName="+ printerName +"&labelBytes="+ event.data;
            printRequest.onreadystatechange = function () {
                if (this.readyState === 4) {
                    var message = {};
                    message.requestType = "response";
                    message.query = this.response;
                    window.opener.postMessage(message, "https://www.ups.com/*");
                }
            }
            printRequest.open("POST", "http://127.0.0.1:4349/print", true);
            printRequest.responseType = "text";
            printRequest.setRequestHeader("Access-Control-Allow-Origin", "http://127.0.0.1:4349"); 
            printRequest.setRequestHeader("Content-type", "application/x-www-form-urlencoded"); 
            printRequest.send(query);
        }
    </script>
    <title>UPS Shipping Label</title>
</head>
<body>
  <div style="font-family:Arial, sans-serif; font-weight:bold; font-size:11px">
    Thanks for shipping with UPS.<br/><br/>
    Your labels have been printed to your UPS thermal printer. If nothing has printed:<ul>
    <li>Confirm you have selected your UPS thermal printer in your printing preferences(see bottom of Complete Shipment page)</li>
    <li>OR select the Install UPS Thermal Printer Link from Printing Preferences to learn more about installing the thermal printer driver and plugin.</li>
    </ul>
    <div id="thermalPrintersDiv">
    <p align="right"><a href="javascript:window.close()"><b>Close Window</b></a></p><input type='hidden' id='thermalPrinterType' value='zpl'></input>
<input type='hidden' id='thermalPrinterName' value='Zebra'></input>

    </div>
  <div id="footerDiv" style="text-align:center; position:fixed; bottom:2%">
Copyright &copy; 2016 United Parcel Service of America, Inc. All rights reserved.
  </div>
  </div>
    <script>
         window.addEventListener("message", receiveMessage, false);
         requestPcl();
    </script>
</body>
</html>
"""

@app.post("/print")
def print_label():
    print(request.path)
    data_raw = request.form['labelBytes']
    data = base64.b64decode(data_raw)
    print(data.decode('ascii'))
    with tempfile.TemporaryDirectory() as tmpdirname:
        fp = open(tmpdirname + '/file', 'wb')
        fp.write(data)
        fp.close()
        lpr("-P", PRINTER_NAME, "-o", "raw", tmpdirname+'/file')
    return "<p>OK"

if __name__ == "__main__":
    app.run(port=4349)
