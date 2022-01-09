
// saves one fm document as html
# target framemaker-16
function saveAsHTML (doc) {
    
    var params = GetSaveDefaultParams ();
    var returnParamsp = new PropVals ();
    
    var saveName = doc.Name.replace (/\.[^\.\\]+$/,".html");
    
    
    //The following declarations walk through the save as process programatically. Each declaration is essential and should remain
    //in it's assigned order.
    
    
    
    //Filter is needed because we can't just save to HTML, we need to call the filter option in the dropdown menu of the popout window.
    var i = GetPropIndex(params, Constants.FS_FileType);
    params[i].propVal.ival = Constants.FV_SaveFmtFilter;
    
    
    //This tells the filter to use the HTML option, which is hardcoded as the string below
    var i = GetPropIndex(params, Constants.FS_SaveFileTypeHint);
    params[i].propVal.sval ="0001ADBEHTML";
    
    doc.Save (saveName, params, returnParamsp);
    
    //Closes the doc after saving.
    doc.Close(Constants.FF_CLOSE_MODIFIED);
}

saveAsHTML (app.ActiveDoc);

