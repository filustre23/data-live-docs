# Allow connections from Hex IP addresses

Many data sources are behind firewalls that require Hex's IP addresses to be allowed (fka "whitelisted") to connect. Depending on your infrastructure, this often means editing your firewall configuration. As a starting point here are reference links for changing network settings for several cloud infrastructures: [AWS](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html), [Azure](https://docs.microsoft.com/en-us/azure/virtual-network/network-security-groups-overview), [Google Cloud](https://cloud.google.com/vpc/docs/firewalls), and [Snowflake](https://docs.snowflake.com/en/user-guide/network-policies.html)

The centrally-hosted Hex Cloud application (e.g. `app.hex.tech`) is served from the following addresses:

```
3.129.36.245  
3.13.16.99  
3.18.79.139
```

For Hex workspaces hosted at `eu.hex.tech`, the following addresses should be added to your allow-list:

```
34.240.244.7  
52.17.12.97  
54.76.153.135
```

For Hex workspaces hosted at `hc.hex.tech`, the following addresses should be added to your allow-list:

```
18.224.164.96  
3.136.150.231  
52.14.118.144
```

For single-tenant customers, the addresses can be found on the right side of the data connection configuration modal.