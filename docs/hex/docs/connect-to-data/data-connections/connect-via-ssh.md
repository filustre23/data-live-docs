On this page

# SSH data connections

## Prepare the SSH host[​](#prepare-the-ssh-host "Direct link to Prepare the SSH host")

### **Prerequisites**[​](#prerequisites "Direct link to prerequisites")

You will need a host in your environment that can access the data source you would like to connect to from Hex. This host is often referred to as a bastion and must have a port [accessible from Hex](/docs/connect-to-data/data-connections/allow-connections-from-hex-ip-addresses). SSH uses port 22 by default.

Currently, Hex supports connecting to the following data sources via SSH tunneling:

* Amazon Athena
* Amazon Redshift
* Databricks\*
* MariaDB
* MySQL (including CloudSQL)
* Postgres (including CloudSQL)
* PrestoDB
* SQL Server (including CloudSQL)
* PrestoDB

info

\*Using an SSH tunnel with Databricks requires the use of an [HTTP proxy](/docs/connect-to-data/data-connections/connect-via-ssh#set-up-an-http-proxy) co-existing on the bastion host

### Configure SSH access[​](#configure-ssh-access "Direct link to Configure SSH access")

On the bastion host, create a group and a user named `hex` then switch to this user. This user will be the SSH user used for tunneling.

tip

If the bastion host already has a user for tunneling, this section may be skipped in favor of using that user.

```
$ sudo groupadd hex  
$ sudo useradd -m -g hex hex  
$ sudo su - hex
```

Create a .ssh directory and authorized\_keys files with appropriate permissions for the hex user.

```
$ mkdir ~/.ssh  
$ chmod 700 ~/.ssh  
$ cd ~/.ssh  
$ touch authorized_keys  
$ chmod 600 authorized_keys
```

### Add your Workspace's Hex SSH public key to the bastion[​](#add-your-workspaces-hex-ssh-public-key-to-the-bastion "Direct link to Add your Workspace's Hex SSH public key to the bastion")

tip

You must be a workspace Admin to access the SSH public key.

Copy the public key from the bottom of the **Settings** → **Data sources** tab, under the "Workspace" header.

Import the public key into the authorized\_keys file using the command below. Please replace `<PUBLIC_KEY>` with the public key.

```
echo "<PUBLIC KEY>" >> ~/.ssh/authorized_keys
```

## Configure data connections to use SSH[​](#configure-data-connections-to-use-ssh "Direct link to Configure data connections to use SSH")

Once your ssh host is prepared with the public key. You can configure your data connections in Hex to use SSH. Toggle **Connect via SSH** on in your data connection configuration and add the details for:

* SSH machine hostname or IP address
* SSH port. This is usually 22.
* SSH username ("hex" in our example)

### SSH Tunneling Architecture Details[​](#ssh-tunneling-architecture-details "Direct link to SSH Tunneling Architecture Details")

* Our client remains within our network perimeter and connects through this tunnel. No client software is installed on your bastion or within your network—it operates as a port forwarding mechanism from our database client into your environment.
* The SSH connection is established on-demand rather than as a persistent tunnel. Each request initiates a new SSH session with appropriate port forwarding for that specific transaction.
* All outbound connections originate from a [dedicated static IP address](/docs/connect-to-data/data-connections/allow-connections-from-hex-ip-addresses) for consistent security policy management.
* Multiple bastion hosts can be configured behind a single DNS entry, providing redundancy and high availability.

### Set up an HTTP proxy[​](#set-up-an-http-proxy "Direct link to Set up an HTTP proxy")

If you're working in a network environment that blocks direct SSH access, which is common in corporate or cloud-managed VPCs, you need to configure an HTTP proxy to establish an SSH tunnel. This setup routes SSH traffic through a proxy server, allowing you to connect securely even when direct outbound access is restricted. You can achieve this using tools like [`squid`](https://www.squid-cache.org/). If you run into connectivity issues, contact [[email protected]](/cdn-cgi/l/email-protection#bbc8cecbcbd4c9cffbd3dec395cfded8d3) for help.

#### On this page

* [Prepare the SSH host](#prepare-the-ssh-host)
  + [**Prerequisites**](#prerequisites)
  + [Configure SSH access](#configure-ssh-access)
  + [Add your Workspace's Hex SSH public key to the bastion](#add-your-workspaces-hex-ssh-public-key-to-the-bastion)
* [Configure data connections to use SSH](#configure-data-connections-to-use-ssh)
  + [SSH Tunneling Architecture Details](#ssh-tunneling-architecture-details)
  + [Set up an HTTP proxy](#set-up-an-http-proxy)