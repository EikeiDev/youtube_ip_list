# iplist-youtube
An attempt to list all IPs that YouTube uses.

This list attempts to keep all ipv4 addresses used by YouTube.
We use DNS Lookups to achieve this and the lists are automatically updated approximately every 5 minutes.
The project is currently STABLE BETA.
So, not all IPs might be available.
At present, it has a collection of
**9789**
YouTube IPs.

Ipv4 list raw link => [Here!](https://raw.githubusercontent.com/EikeiDev/iplist-youtube/refs/heads/main/ipv4_list.txt)

***New!*** CIDR List => [Here!](https://raw.githubusercontent.com/EikeiDev/iplist-youtube/refs/heads/main/cidr4.txt)

#### How to make the lists manually.
There are one script in the repository root, `list_generator.py`.
Running any of these scripts should generate one file with a list of **IPv4** addresses with the filenames `ipv4_list.txt`.
It has a little chance of listing some wrong **IPs** In some cases.
With a warning or error.

For the `.py` file, you need to install dependencies.
This is only necessary once.
```bash
pip3 install -r requirements.txt
```
Then run:
```bash
chmod +x list_generator.py
./list_generator.py
```
If this doesn't work, try:
```bash
python3 list_generator.py
```
***New!*** To generate CIDR lists use `generate_cidr.py`
```py
python3 generate_cidr.py
```
#### Important Notes
Using any of these scripts once is not enough.
This is because **IPs** returned by DNS Queries are not consistent.
They are changed at fixed or unfixed intervals.
Although all **IPs** are not returned at the same time, all have the same purpose.
And different computers use different **IPs** at the same time.
And so, running the scripts, again and again, is a necessity.
If you run the scripts more **IPs** should be automatic.
Personally recommend running the scripts at least **100** times at the interval of **5** minutes or **300** seconds (Google's TTL).
For reasonable performance, run it **1000** times before using it for production.
I use such Cron jobs to populate the lists.
```cron
*/5 * * * * /path/to/the/script
```
