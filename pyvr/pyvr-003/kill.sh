ps xa | grep "python" | grep pyvr | awk -F ' '  {'print $1'} | xargs kill
