% Define the path where analysis files are located
analysisPath = fullfile('/Users','jasper','NMF','temporalfrontal');

% Iterate through each number of components, each subject, and each hemisphere
for compNumb = ["50" "60" "100" "200"]
    for subject = ["subj1" "subj2" "subj3"]
        for hemi = ['L' 'R']
            % Load OFC and PFC ROIs
            OFCmask = readimgfile(char(fullfile(analysisPath,strcat(hemi,'_ofc_stable.func.gii'))));
            PFCmask = readimgfile(char(fullfile(analysisPath,strcat(hemi,'_pfc_stable.func.gii'))));

            % Load the occipital-frontal component
            OFComp = readimgfile(char(fullfile(analysisPath,subject,'/separated_OF/',strcat('OF_',hemi,compNumb,'.func.gii'))));
            
            % Calculate the OFC mask vs. PFC mask size ratio
            sizeRatio = calcSizeProp(OFCmask,PFCmask);

            % Calculate how much of the frontal termination site is captured by OFC vs. PFC
            OFProp = calcOFProp(OFComp,OFCmask,PFCmask);

            % Display output
            disp(strcat(subject," ",compNumb," components, ",hemi," hemisphere"));
            disp(strcat("OFC is ",num2str(sizeRatio)," of PFC, yet OFC captures ",num2str(OFProp)," of the O-F connection."));
        end
    end
end

% Function to calculate the size of the OFC mask vs. the PFC mask
function sizeRatio = calcSizeProp(OFCmask,PFCmask)
    sizeOFC = sum(OFCmask>0);
    sizePFC = sum(PFCmask>0);
    sizeRatio = sizeOFC ./ sizePFC;
end

% Function to calculate what proportion of occipital-frontal component is captured by OFC vs. PFC
function OFProp = calcOFProp(OFComp,OFCmask,PFCmask)
    OFCsum = sum(OFComp(find(OFCmask>0)));
    PFCsum = sum(OFComp(find(PFCmask>0)));
    OFProp = OFCsum ./ PFCsum;
end