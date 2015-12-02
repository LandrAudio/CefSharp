import ConfigParser
import sys
import os
import subprocess

def build_cef(config):
    cmd = 'python automate-git.py --download-dir=cef --branch={0} --no-debug-build'.format(
       config.get('cef', 'branch'))

    cmd_parts = cmd.split();

    env = os.environ
    env['GYP_GENERATORS'] = 'ninja,msvs-ninja'
    env['GYP_MSVS_VERSION'] = '2013'
    env['GYP_DEFINES'] = 'proprietary_codecs=1 ffmpeg_branding=Chrome'

    process = subprocess.Popen(cmd_parts, env=env,
                               stdout=sys.stdout,
                               stderr=sys.stderr)
    
    out, err = process.communicate() 
        
def pack_cef(config):
    cmd = '.\\nuget\\NuGet.exe pack .\\NuGet\\cef.redist.nuspec -NoPackageAnalysis -Version {0} -OutputDirectory .\\NuGet\\ -Properties Configuration=Release;Platform=x86;'.format(
        config.get('cef', 'version'))
    
    cmd_parts = cmd.split()
    process = subprocess.Popen(cmd_parts,
                               stdout=sys.stdout,
                               stderr=sys.stderr)
    
    out, err = process.communicate() 

def build_cefsharp(config):
    cmd = 'powershell -ExecutionPolicy RemoteSigned -File build.ps1 vs2013 {0} {1} {2}'.format(
        config.get('cefsharp', 'version'), #Version
        config.get('cefsharp', 'version'), #AssemblyVersion
        config.get('cef', 'version'))
    
    cmd_parts = cmd.split();
    process = subprocess.Popen(cmd_parts, 
                               stdout=sys.stdout,
                               stderr=sys.stderr)
    
    out, err = process.communicate() 

##
# Program entry point.
##

config = ConfigParser.ConfigParser()
config.read('build.ini')

build_cef(config)
pack_cef(config)
build_cefsharp(config)