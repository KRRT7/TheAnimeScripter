var panelGlobal = this;
var TheAnimeScripter = (function() {

    var scriptName = "TheAnimeScripter";
    var scriptVersion = "0.1.1";
    var scriptAuthor = "Nilas";
    var scriptURL = "https://github.com/NevermindNilas/TheAnimeScripter"
    var discordServer = "https://discord.gg/CdRD9GwS8J"

    // Default Values for the settings
    var outputFolder = app.settings.haveSetting(scriptName, "outputFolder") ? app.settings.getSetting(scriptName, "outputFolder") : "undefined";
    var TheAnimeScripterPath = app.settings.haveSetting(scriptName, "TheAnimeScripterPath") ? app.settings.getSetting(scriptName, "TheAnimeScripterPath") : "undefined";
    var dropdownModel = app.settings.haveSetting(scriptName, "dropdownModel") ? app.settings.getSetting(scriptName, "dropdownModel") : 0;
    var dropdownCugan = app.settings.haveSetting(scriptName, "dropdownCugan") ? app.settings.getSetting(scriptName, "dropdownCugan") : 0;
    var dropdownSwinIr = app.settings.haveSetting(scriptName, "dropdownSwinIr") ? app.settings.getSetting(scriptName, "dropdownSwinIr") : 0;
    var dropdwonSegment = app.settings.haveSetting(scriptName, "dropdwonSegment") ? app.settings.getSetting(scriptName, "dropdwonSegment") : 0;
    var intInterpolate = app.settings.haveSetting(scriptName, "intInterpolate") ? app.settings.getSetting(scriptName, "intInterpolate") : 2;
    var intUpscale = app.settings.haveSetting(scriptName, "intUpscale") ? app.settings.getSetting(scriptName, "intUpscale") : 2;
    var intNumberOfThreads = app.settings.haveSetting(scriptName, "intNumberOfThreads") ? app.settings.getSetting(scriptName, "intNumberOfThreads") : 1;
    var segmentValue = 0;
    // THEANIMESCRIPTER
    // ================
    var TheAnimeScripter = (panelGlobal instanceof Panel) ? panelGlobal : new Window("palette");
    if (!(panelGlobal instanceof Panel)) TheAnimeScripter.text = "TheAnimeScripter";
    TheAnimeScripter.orientation = "column";
    TheAnimeScripter.alignChildren = ["center", "top"];
    TheAnimeScripter.spacing = 10;
    TheAnimeScripter.margins = 10;

    // PANELCHAIN
    // ==========
    var panelChain = TheAnimeScripter.add("panel", undefined, undefined, {
        name: "panelChain"
    });
    panelChain.text = "Chain";
    panelChain.orientation = "column";
    panelChain.alignChildren = ["left", "top"];
    panelChain.spacing = 10;
    panelChain.margins = 10;

    var buttonStartProcess = panelChain.add("button", undefined, undefined, {
        name: "buttonStartProcess"
    });
    buttonStartProcess.text = "Start  Process";
    buttonStartProcess.preferredSize.width = 104;
    buttonStartProcess.alignment = ["center", "top"];

    // GROUP1
    // ======
    var group1 = panelChain.add("group", undefined, {
        name: "group1"
    });
    group1.orientation = "row";
    group1.alignChildren = ["left", "center"];
    group1.spacing = 10;
    group1.margins = 0;

    var checkboxDeduplicate = group1.add("checkbox", undefined, undefined, {
        name: "checkboxDeduplicate"
    });
    checkboxDeduplicate.alignment = ["left", "center"];

    var textDeduplicate = group1.add("statictext", undefined, undefined, {
        name: "textDeduplicate"
    });
    textDeduplicate.text = "Deduplicate";
    textDeduplicate.justify = "center";
    textDeduplicate.alignment = ["left", "center"];
    textDeduplicate.helpTip = "Deduplicate using FFMPEG's mpdecimate filter";

    // GROUP2
    // ======
    var group2 = panelChain.add("group", undefined, {
        name: "group2"
    });
    group2.orientation = "row";
    group2.alignChildren = ["left", "center"];
    group2.spacing = 10;
    group2.margins = 0;

    var checkboxUpscale = group2.add("checkbox", undefined, undefined, {
        name: "checkboxUpscale"
    });
    checkboxUpscale.alignment = ["left", "center"];

    var textUpscale = group2.add("statictext", undefined, undefined, {
        name: "textUpscale"
    });
    textUpscale.text = "Upscale";
    textUpscale.justify = "center";
    textUpscale.alignment = ["left", "center"];
    textUpscale.helpTip = "Upscale using the model you choose";

    // GROUP3
    // ======
    var group3 = panelChain.add("group", undefined, {
        name: "group3"
    });
    group3.orientation = "row";
    group3.alignChildren = ["left", "center"];
    group3.spacing = 10;
    group3.margins = 0;

    var checkboxInterpolate = group3.add("checkbox", undefined, undefined, {
        name: "checkboxInterpolate"
    });
    checkboxInterpolate.alignment = ["left", "center"];

    var textInterpolate = group3.add("statictext", undefined, undefined, {
        name: "textInterpolate"
    });
    textInterpolate.text = "Interpolate";
    textInterpolate.justify = "center";
    textInterpolate.alignment = ["left", "center"];
    textInterpolate.helpTip = "Interpolate using RIFE - current model supported 4.13.2";
    
    var group4 = panelChain.add("group", undefined, {
        name: "group4"
    });

    var checkboxSharpen = group4.add("checkbox", undefined, undefined, {
        name: "checkboxSharpen"
    });

    checkboxSharpen.alignment = ["left", "center"];

    var textSharpen = group4.add("statictext", undefined, undefined, {
        name: "textSharpen"
    });
    textSharpen.text = "Sharpen";
    textSharpen.justify = "center";
    textSharpen.alignment = ["left", "center"];
    textSharpen.helpTip = "Sharpen using Contrast Adaptive Sharpening";


    // panelPostProcess
    // ==========
    var panelPostProcess = TheAnimeScripter.add("panel", undefined, undefined, {
        name: "panelPostProcess"
    });
    panelPostProcess.text = "Post Process";
    panelPostProcess.orientation = "column";
    panelPostProcess.alignChildren = ["left", "top"];
    panelPostProcess.spacing = 10;
    panelPostProcess.margins = 10;

    var buttonDepthMap = panelPostProcess.add("button", undefined, undefined, {
        name: "buttonDepthMap"
    });
    buttonDepthMap.enabled = false;
    buttonDepthMap.text = "Depth Map";
    buttonDepthMap.preferredSize.width = 105;
    buttonDepthMap.alignment = ["center", "top"];

    var buttonSegment = panelPostProcess.add("button", undefined, undefined, {
        name: "buttonSegment"
    });
    buttonSegment.text = "Segment";
    buttonSegment.preferredSize.width = 105;

    // PANELMORE
    // =========
    var panelMore = TheAnimeScripter.add("panel", undefined, undefined, {
        name: "panelMore"
    });
    panelMore.text = "More";
    panelMore.orientation = "column";
    panelMore.alignChildren = ["left", "top"];
    panelMore.spacing = 10;
    panelMore.margins = 10;

    var buttonInfo = panelMore.add("button", undefined, undefined, {
        name: "buttonInfo"
    });
    buttonInfo.text = "Info";
    buttonInfo.preferredSize.width = 105;
    buttonInfo.alignment = ["center", "top"];
    buttonInfo.enabled = false;

    var buttonSettings = panelMore.add("button", undefined, undefined, {
        name: "buttonSettings"
    });
    buttonSettings.text = "Settings";
    buttonSettings.preferredSize.width = 105;
    buttonSettings.alignment = ["center", "top"];

    TheAnimeScripter.layout.layout(true);
    TheAnimeScripter.layout.resize();
    TheAnimeScripter.onResizing = TheAnimeScripter.onResize = function() {
        this.layout.resize();
    }

    var settingsWindow = new Window("palette", undefined, undefined, {
        resizable: true,
        closeButton: false
    });

    settingsWindow.text = "Settings";
    settingsWindow.orientation = "column";
    settingsWindow.alignChildren = ["center", "top"];
    settingsWindow.spacing = 10;
    settingsWindow.margins = 10;

    // PANELONFIRSTRUN
    // ===============
    var panelOnFirstRun = settingsWindow.add("panel", undefined, undefined, {
        name: "panelOnFirstRun"
    });
    panelOnFirstRun.text = "On First Run";
    panelOnFirstRun.orientation = "column";
    panelOnFirstRun.alignChildren = ["left", "top"];
    panelOnFirstRun.spacing = 10;
    panelOnFirstRun.margins = 10;

    // GROUP1
    // ======
    var group1 = panelOnFirstRun.add("group", undefined, {
        name: "group1"
    });
    group1.orientation = "row";
    group1.alignChildren = ["left", "center"];
    group1.spacing = 10;
    group1.margins = 0;

    var buttonFolder = group1.add("button", undefined, undefined, {
        name: "buttonFolder"
    });
    buttonFolder.helpTip = "Set it to wherever The Anime Scripter folder is situated.";
    buttonFolder.text = "Set Folder";
    buttonFolder.preferredSize.width = 100;

    var buttonOutput = group1.add("button", undefined, undefined, {
        name: "buttonOutput"
    });
    buttonOutput.text = "Set Output";
    buttonOutput.preferredSize.width = 101;
    buttonOutput.helpTip = "Set it to wherever you want the output to be saved.";
    // GENERALPANEL
    // ============
    var generalPanel = settingsWindow.add("panel", undefined, undefined, {
        name: "generalPanel"
    });
    generalPanel.text = "General";
    generalPanel.orientation = "column";
    generalPanel.alignChildren = ["left", "top"];
    generalPanel.spacing = 10;
    generalPanel.margins = 10;

    var textSharpen = generalPanel.add("statictext", undefined, undefined, {
        name: "textSharpen"
    });
    textSharpen.text = "Sharpen";
    textSharpen.justify = "center";
    textSharpen.alignment = ["center", "top"];

    var sliderSharpen = generalPanel.add("slider", undefined, undefined, undefined, undefined, {
        name: "sliderSharpen"
    });
    sliderSharpen.minvalue = 0;
    sliderSharpen.maxvalue = 100;
    sliderSharpen.value = 50;
    sliderSharpen.preferredSize.width = 212;
    sliderSharpen.alignment = ["center", "top"];

    var labelSharpen = generalPanel.add("statictext", undefined, sliderSharpen.value + "%", {
        name: "labelSharpen"
    });
    labelSharpen.alignment = ["center", "top"];

    sliderSharpen.onChange = function() {
        labelSharpen.text = Math.round(sliderSharpen.value) + "%";
    }

    // GROUP2
    // ======
    var group2 = generalPanel.add("group", undefined, {
        name: "group2"
    });
    group2.orientation = "row";
    group2.alignChildren = ["left", "center"];
    group2.spacing = 0;
    group2.margins = 0;

    var textInterpolationMultiplier = group2.add("statictext", undefined, undefined, {
        name: "textInterpolationMultiplier"
    });
    textInterpolationMultiplier.text = "Interpolation Multiplier";
    textInterpolationMultiplier.preferredSize.width = 172;
    textInterpolationMultiplier.alignment = ["left", "center"];

    var intInterpolate = group2.add('edittext {justify: "center", properties: {name: "intInterpolate"}}');
    intInterpolate.text = "2";
    intInterpolate.preferredSize.width = 40;
    intInterpolate.alignment = ["left", "center"];

    // GROUP3
    // ======
    var group3 = generalPanel.add("group", undefined, {
        name: "group3"
    });
    group3.orientation = "row";
    group3.alignChildren = ["left", "center"];
    group3.spacing = 0;
    group3.margins = 0;

    var textUpscaleMultiplier = group3.add("statictext", undefined, undefined, {
        name: "textUpscaleMultiplier"
    });
    textUpscaleMultiplier.text = "Upscale Multiplier";
    textUpscaleMultiplier.preferredSize.width = 172;

    var intUpscale = group3.add('edittext {justify: "center", properties: {name: "intUpscale"}}');
    intUpscale.text = "2";
    intUpscale.preferredSize.width = 40;
    intUpscale.alignment = ["left", "top"];

    // GROUP4
    // ======
    var group4 = generalPanel.add("group", undefined, {
        name: "group4"
    });
    group4.orientation = "row";
    group4.alignChildren = ["left", "center"];
    group4.spacing = 0;
    group4.margins = 0;

    var textNumberOfThreads = group4.add("statictext", undefined, undefined, {
        name: "textNumberOfThreads"
    });
    textNumberOfThreads.enabled = false;
    textNumberOfThreads.text = "Number of Threads";
    textNumberOfThreads.preferredSize.width = 172;

    var intNumberOfThreads = group4.add('edittext {justify: "center", properties: {name: "intNumberOfThreads"}}');
    intNumberOfThreads.enabled = false;
    intNumberOfThreads.text = "1";
    intNumberOfThreads.preferredSize.width = 40;

    // PANEL1
    // ======
    var panel1 = settingsWindow.add("panel", undefined, undefined, {
        name: "panel1"
    });
    panel1.text = "Model Picker";
    panel1.orientation = "column";
    panel1.alignChildren = ["left", "top"];
    panel1.spacing = 10;
    panel1.margins = 10;

    // GROUP5
    // ======
    var group5 = panel1.add("group", undefined, {
        name: "group5"
    });
    group5.orientation = "row";
    group5.alignChildren = ["left", "center"];
    group5.spacing = 0;
    group5.margins = 0;

    var textUpscaleModel = group5.add("statictext", undefined, undefined, {
        name: "textUpscaleModel"
    });
    textUpscaleModel.text = "Upscale Model";
    textUpscaleModel.preferredSize.width = 103;

    var dropdownModel_array = ["ShuffleCugan", "-", "Compact", "-", "UltraCompact", "-", "SuperUltraCompact", "-", "Cugan", "-", "Cugan-AMD", "-", "SwinIR"];
    var dropdownModel = group5.add("dropdownlist", undefined, undefined, {
        name: "dropdownModel",
        items: dropdownModel_array
    });
    dropdownModel.helpTip = "Choose which model you want to utilize, ordered by speed, read more in INFO";
    dropdownModel.selection = 0;
    dropdownModel.preferredSize.width = 109;

    // GROUP6
    // ======
    var group6 = panel1.add("group", undefined, {
        name: "group6"
    });
    group6.orientation = "row";
    group6.alignChildren = ["left", "center"];
    group6.spacing = 0;
    group6.margins = 0;

    var cuganDenoiseText = group6.add("statictext", undefined, undefined, {
        name: "cuganDenoiseText"
    });
    cuganDenoiseText.text = "Cugan Denoise";
    cuganDenoiseText.preferredSize.width = 103;

    var dropdownCugan_array = ["No-Denoise", "-", "Conservative", "-", "Denoise1x", "-", "Denoise2x"];
    var dropdownCugan = group6.add("dropdownlist", undefined, undefined, {
        name: "dropdownCugan",
        items: dropdownCugan_array
    });
    dropdownCugan.selection = 0;
    dropdownCugan.preferredSize.width = 109;

    // GROUP10
    var buttonSettingsClose = settingsWindow.add("button", undefined, undefined, {
        name: "buttonSettingsClose"
    });
    buttonSettingsClose.text = "Close";

    buttonSettingsClose.onClick = function() {
        settingsWindow.hide();
    }

    buttonOutput.onClick = function() {
        var folder = Folder.selectDialog("Select Output folder");
        if (folder != null) {
            alert("Stored the output folder, this will be saved in memory until you change it again")
            outputFolder = folder.fsName;
            app.settings.saveSetting(scriptName, "outputFolder", outputFolder);
        }
    };

    buttonFolder.onClick = function() {
        var folder = Folder.selectDialog("Select The Anime Scripter folder");
        if (folder != null) {
            alert("Stored the The Anime Scripter folder, this will be saved in memory until you change it again")
            TheAnimeScripterPath = folder.fsName;
            app.settings.saveSetting(scriptName, "TheAnimeScripterPath", TheAnimeScripterPath);
        }
    };

    dropdownModel.onChange = function() {
        app.settings.saveSetting(scriptName, "dropdownModel", dropdownModel.selection.index);
    }

    dropdownCugan.onChange = function() {
        app.settings.saveSetting(scriptName, "dropdownCugan", dropdownCugan.selection.index);
    }

    dropdownSwinIr.onChange = function() {
        app.settings.saveSetting(scriptName, "dropdownSwinIr", dropdownSwinIr.selection.index);
    }

    dropdwonSegment.onChange = function() {
        app.settings.saveSetting(scriptName, "dropdwonSegment", dropdwonSegment.selection.index);
    }

    intInterpolate.onChange = function() {
        app.settings.saveSetting(scriptName, "intInterpolate", intInterpolate.text);
    }

    intUpscale.onChange = function() {
        app.settings.saveSetting(scriptName, "intUpscale", intUpscale.text);
    }

    intNumberOfThreads.onChange = function() {
        app.settings.saveSetting(scriptName, "intNumberOfThreads", intNumberOfThreads.text);
    }

    buttonSettings.onClick = function() {
        settingsWindow.show();
    };

    sliderSharpen.onChange = function() {
        app.settings.saveSetting(scriptName, "sliderSharpen", sliderSharpen.value);
    }


    // START PROCESS FUNCTION
    buttonStartProcess.onClick = function() {
        if (checkboxDeduplicate.value == false && checkboxUpscale.value == false && checkboxInterpolate.value == false && checkboxSharpen.value == false) {
            alert("Please select at least one of the checkboxes");
            return;
        }
        
        start_chain();
    }

    buttonSegment.onClick = function() {
        segmentValue = 1;
        start_chain();
    }

    function callCommand(command) {
        try {
            var cmdCommand = 'cmd.exe /c "' + command + '"';

            system.callSystem(cmdCommand);

            // Added because the metadata would only finish writing after the script was done, I assume.
            $.sleep(500);
        } catch (error) {
            alert(error);
            alert("Something went wrong trying to process the chain, please contact me on discord")
        }
    }

    function start_chain() {
        if (((!app.project) || (!app.project.activeItem)) || (app.project.activeItem.selectedLayers.length < 1)) {
            alert("Please select one layer.");
            return;
        }

        if (outputFolder == "undefined" || outputFolder == null) {
            alert("The output folder has not been selected, please go to settings");
            return;
        }

        if (TheAnimeScripterPath == "undefined" || TheAnimeScripterPath == null) {
            alert("The Anime Scripter directory has not been selected, please go to settings");
            return;
        }

        if (app.preferences.getPrefAsLong("Main Pref Section v2", "Pref_SCRIPTING_FILE_NETWORK_SECURITY") != 1) {
            alert("Please tick the \"Allow Scripts to Write Files and Access Network\" checkbox in Scripting & Expressions");
            return app.executeCommand(2359);
        }

        var exeFile = TheAnimeScripterPath + "\\main.exe";
        var activeItem = app.project.activeItem;

        var comp = app.project.activeItem;
        for (var i = 0; i < comp.selectedLayers.length; i++) {
            var layer = comp.selectedLayers[i];
            var activeLayerPath = layer.source.file.fsName;
            var activeLayerName = layer.name;

            var inPoint = layer.inPoint;
            var outPoint = layer.outPoint;
            var duration = outPoint - inPoint;

            if (duration == layer.source.duration) {
                inPoint = 0;
                outPoint = 0;
            }

            var randomNumber = Math.floor(Math.random() * 1000000);
            output_name = outputFolder + "\\" + activeLayerName.replace(/\.[^\.]+$/, '') + "_" + randomNumber + ".mp4";

            try {
                var attempt = [
                    "cd", "\"" + TheAnimeScripterPath + "\"", 
                    "&&", 
                    "\"" + exeFile + "\"", 
                    "--input", "\"" + activeLayerPath + "\"", 
                    "--output", "\"" + output_name + "\"", 
                    "--interpolate", checkboxInterpolate.value ? "1" : "0", 
                    "--interpolate_factor", intInterpolate.text, 
                    "--upscale", checkboxUpscale.value ? "1" : "0", 
                    "--upscale_factor", intUpscale.text, 
                    "--dedup", checkboxDeduplicate.value ? "1" : "0", 
                    "--half", "1",
                    "--upscale_method", dropdownModel.selection.text,
                    "--inpoint", inPoint,
                    "--outpoint", outPoint,
                    "--sharpen", checkboxSharpen.value ? "1" : "0",
                    "--sharpen_sens", sliderSharpen.value,
                    "--segment", segmentValue, 


                ];
                var command = attempt.join(" ");
            } catch (error) {
                alert(error);
            }

            alert (command);
            callCommand(command);

            $.sleep(500);
            try {
                var importOptions = new ImportOptions(File(output_name));
                var importedFile = app.project.importFile(importOptions);
                var inputLayer = comp.layers.add(importedFile);
                inputLayer.moveBefore(layer);
                if (checkboxUpscale.value == true) {
                    var compWidth = comp.width;
                    var compHeight = comp.height;
                    var layerWidth = inputLayer.source.width;
                    var layerHeight = inputLayer.source.height;
                    var scaleX = (compWidth / layerWidth) * 100;
                    var scaleY = (compHeight / layerHeight) * 100;
                    inputLayer.property("Scale").setValue([scaleX, scaleY, 100]);
                }
            } catch (error) {
                alert(error);
                alert("Something went wrong trying to import the file, please look at the output folder");
            } 
        }
    }
    if (TheAnimeScripter instanceof Window) TheAnimeScripter.show();
    return TheAnimeScripter;
}());