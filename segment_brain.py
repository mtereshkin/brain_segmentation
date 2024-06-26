import subprocess

if __name__ == "__main__":
    command = "antsBrainExtraction.sh -d 3 -a CT2.nii.gz -e templates/T_template0.nii.gz  -m templates/T_template0_BrainCerebellumProbabilityMask.nii.gz -o output"
    subprocess.run(command, shell=True)