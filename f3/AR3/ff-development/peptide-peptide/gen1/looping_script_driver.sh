#!/usr/bin/bash

# take an input file and modify it with some sed command
# force matching: change fpb and step over relevant ranges

TEMPLATE_FILE=fm_settings.txt
SETTINGS_DIR=fm-settings
TRAJ=traj_aa25_400-500.trr
CG_MAP_1=second_cg.xml
CG_MAP_2=water.xml
TOPOL=topol_fm.tpr
VAR_TEXT_1=FPB
VAR_TEXT_2=MIN_R
VAR_TEXT_3=STEP_SIZE
VAR_TEXT_4=INTERACTION
VAR_TEXT_5=BEAD_TYPE_1
VAR_TEXT_6=BEAD_TYPE_2
SCRIPT_DIR=fm-scripts
PROJECT_ROOT_DIR=$PWD

for frames_per_block in {1000..3000..1000};
do
    for min_r in {25..46..03}; 
    do
        for step_size in {05..09..02}; 
        do
            for nonbond in \
            NH3-NH3 NH3-CA NH3-AMD NH3-PHA NH3-PHB \
            NH3-PHC NH3-COO CA-CA CA-AMD CA-PHA \
            CA-PHB CA-PHC CA-COO AMD-AMD AMD-PHA \
            AMD-PHB AMD-PHC AMD-COO PHA-PHA PHA-PHB \
            PHA-PHC PHA-COO PHB-PHB PHB-PHC PHB-COO \
            PHC-PHC PHC-COO COO-COO
            do
                cd $PROJECT_ROOT_DIR
                if [[ ! -d $nonbond ]]
                then
                    mkdir $nonbond 
                fi
                cd $nonbond
                
                run_name=fpb$frames_per_block-min$min_r-step$step_size
                if [[ ! -d $run_name ]]
                then
                    mkdir $run_name
                fi
                cd $run_name
                
                bead_type_1=`echo $nonbond | grep -oE "^[[:alnum:]]+"`
                bead_type_2=`echo $nonbond | grep -oE "[[:alnum:]]+$"`
                
                sed -e "s/${VAR_TEXT_1}/${frames_per_block}/g" \
                    -e "s/${VAR_TEXT_2}/${min_r}/g" \
                    -e "s/${VAR_TEXT_3}/${step_size}/g" \
                    -e "s/${VAR_TEXT_4}/${nonbond}/g" \
                    -e "s/${VAR_TEXT_5}/${bead_type_1}/g" \
                    -e "s/${VAR_TEXT_6}/${bead_type_2}/g" \
                    $PROJECT_ROOT_DIR/$TEMPLATE_FILE \
                    > settings_FM_$nonbond.xml
                
                cp -a $PROJECT_ROOT_DIR/$SCRIPT_DIR/run_FM_$nonbond.sh ./
                
                ln -s $PROJECT_ROOT_DIR/$TRAJ traj.trr
                ln -s $PROJECT_ROOT_DIR/$CG_MAP_1 second_cg.xml
                ln -s $PROJECT_ROOT_DIR/$CG_MAP_2 water.xml
                ln -s $PROJECT_ROOT_DIR/$TOPOL topol_fm.tpr
                
                sbatch run_FM_$nonbond.sh
            done; 
        done;
    done;
done;
