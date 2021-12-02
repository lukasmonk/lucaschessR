#!/bin/bash

echo ""
echo ":: Building CpuUtil"
echo ""

cd ./source

python3 setup_cpuutil.py build_ext --inplace --verbose

cp CpuUtil.cpython-3* ../../OS/darwin

echo ""
echo ":: Building CpuUtil Complete"
echo ""
