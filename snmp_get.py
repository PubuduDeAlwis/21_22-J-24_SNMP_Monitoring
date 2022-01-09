import subprocess

cpu_load_1min = ".1.3.6.1.4.1.2021.10.1.3.1"
cpu_load_5min = ".1.3.6.1.4.1.2021.10.1.3.2"
cpu_load_15min = ".1.3.6.1.4.1.2021.10.1.3.3"
idle_cpu_time = ".1.3.6.1.4.1.2021.11.11.0"
real_total_RAM = ".1.3.6.1.4.1.2021.4.5.0"
real_available_RAM = ".1.3.6.1.4.1.2021.4.6.0"
membuffer = ".1.3.6.1.4.1.2021.4.14.0"
memcache = "1.3.6.1.4.1.2021.4.15.0"
available_disk_space = ".1.3.6.1.4.1.2021.9.1.7.1"
used_disk_space = ".1.3.6.1.4.1.2021.9.1.8.1" 


def snmp_get():
	cpu_1min = subprocess.Popen(["snmpget", "-c", "public" , "-v1", "localhost", cpu_load_1min], stdin=subprocess.PIPE, stdout=subprocess.PIPE, 
	text=True)
	cpu_5min = subprocess.Popen(["snmpget", "-c", "public", "-v1", "localhost", cpu_load_5min], stdin=subprocess.PIPE, stdout=subprocess.PIPE, 
	text=True)
	cpu_15min = subprocess.Popen(["snmpget", "-c", "public", "-v1", "localhost", cpu_load_15min], stdin=subprocess.PIPE, stdout=subprocess.PIPE, 
	text=True)
	cpu_idle = subprocess.Popen(["snmpget", "-c", "public", "-v1", "localhost", idle_cpu_time], stdin=subprocess.PIPE, stdout=subprocess.PIPE, 
	text=True)

	real_total_ram = subprocess.Popen(["snmpget", "-c", "public", "-v1", "localhost", real_total_RAM], stdin=subprocess.PIPE, stdout=subprocess.PIPE, 
	text=True)	
	real_available_ram = subprocess.Popen(["snmpget", "-c", "public", "-v1", "localhost", real_available_RAM], stdin=subprocess.PIPE, 
	stdout=subprocess.PIPE, text=True)
	buffer = subprocess.Popen(["snmpget", "-c", "public", "-v1", "localhost", membuffer], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
	cache = subprocess.Popen(["snmpget", "-c", "public", "-v1", "localhost", memcache], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

	#free_disk_space = subprocess.Popen(["snmpget", "-c", "public", "-v1", "localhost", available_disk_space], stdin=subprocess.PIPE, 
	#stdout=subprocess.PIPE,text=True)
	#use_disk_space = subprocess.Popen(["snmpget", "-c", "public", "-v1", "localhost", used_disk_space], stdin=subprocess.PIPE, 
	#stdout=subprocess.PIPE, text=True)

	output_cpu_1min = cpu_1min.communicate()[0].split(":")
	output_cpu_5min = cpu_5min.communicate()[0].split(":")
	output_cpu_15min = cpu_15min.communicate()[0].split(":")
	output_cpu_idle = cpu_idle.communicate()[0].split(":")



	output_total_ram = real_total_ram.communicate()[0].split(":")
	tot_RAM = int(output_total_ram[1])

	output_available_ram = real_available_ram.communicate()[0].split(":")
	tot_available_ram = int(output_available_ram[1])

	output_buffer = buffer.communicate()[0].split(":")
	tot_buffer = int(output_buffer[1])

	output_cache = cache.communicate()[0].split(":")
	tot_cache = int(output_cache[1])

	memoryutilization = round((tot_available_ram + tot_buffer + tot_cache)/tot_RAM, 2)

	#output_free_disk_space = free_disk_space.communicate()[0]
	#output_use_disk_space = use_disk_space.communicate()[0]
	monitoring_output = """\
<!DOCTYPE html>
<html>
    <body>
        <center><h1 style="color:SlateGray;">Server Resource</h1></center>
	<center><table>
		<tr>
			<th style="text-align:center">Resource Type</th>
			<th style="text-align:center">Useage Amount</th>
		</tr>
		<tr>
			<td style="text-align:center">CPU Load 1min</td>
			<td style="text-align:center">{output_cpu_1min}</td>
		</tr>
		<tr>
			<td style="text-align:center">CPU Load 5min</td>
			<td style="text-align:center">{output_cpu_5min}</td>
		</tr>
		<tr>
			<td style="text-align:center">CPU Load 15min</td>
			<td style="text-align:center">{output_cpu_15min}</td>
		</tr>
		<tr>
			<td style="text-align:center">Total RAM</td>
			<td style="text-align:center">{tot_RAM}</td>
		</tr>
		<tr>
			<td style="text-align:center">Total Available RAM</td>
			<td style="text-align:center">{tot_available_ram}</td>
		</tr>
		<tr>
			<td style="text-align:center">Memory Buffer</td>
			<td style="text-align:center">{tot_buffer}</td>
		</tr>
		<tr>
			<td style="text-align:center">Cache Memory</td>
			<td style="text-align:center">{tot_cache}</td>
		</tr>
		<tr>
			<td style="text-align:center">Memory Utilization</td>
			<td style="text-align:center">{memoryutilization}</td>
		</tr>
	</table></center>
    </body>
</html>
""".format(output_cpu_1min=output_cpu_1min[1], output_cpu_5min=output_cpu_5min[1], output_cpu_15min=output_cpu_15min[1], tot_RAM=tot_RAM, 
tot_available_ram=tot_available_ram, tot_buffer=tot_buffer, tot_cache=tot_cache, memoryutilization=memoryutilization)

	#monitoring_output= f"cpu_load_1min: {output_cpu_1min[1]}cpu_load_5min: {output_cpu_5min[1]}cpu_load_15min: {output_cpu_15min[1]}" \
	#f"total_RAM: {tot_RAM}\ntotal_available_RAM: {tot_available_ram}\nMemory_Buffer: {tot_buffer}\nCache_Memory: {tot_cache}\n" \
	#f"Memory_Utilization: {memoryutilization} \n" \
	#print (f"free_disk_space: {output_free_disk_space}")
	#print (f"used_disk_space: {output_use_disk_space}")
	return monitoring_output

monitoring = snmp_get()
	
print(monitoring)
