
class ibrdtn_config {
    file { "/etc/ibrdtn/ibrdtnd.conf":
        ensure => present,
        mode => 666,
        owner => root,
        group => root,
        source =>"puppet://os/files/ibrdtnd.conf"
    }
}

class time_execute {
    file { "/usr/bin/te":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/te"
    }
}

class killdtn_file {
    file { "/usr/bin/killdtn":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/killdtn"
    }
}

class killagent_file {
    file { "/usr/bin/killagent":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/killagent"
    }
}

class netem-agent_file {
    file { "/usr/bin/netem-agent":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/netem-agent"
    }
}
class time_iptables{
    file {"/usr/bin/test_time":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/test_time"
    }

}

class test_time{
    exec {"test_time":
        path => "/usr/bin/:/usr/sbin/:/usr/local/bin:/usr/local/sbin:/sbin/:/bin"
    }
}

class killdtn{
    exec {"killdtn":
        path => "/usr/bin/:/usr/sbin/:/usr/local/bin:/usr/local/sbin:/sbin/:/bin"
    }
}

class killagent{
    exec {"killagent":
        path => "/usr/bin/:/usr/sbin/:/usr/local/bin:/usr/local/sbin:/sbin/:/bin"
    }
}

class pre_command {
    exec {"mount -t nfs 192.168.99.112:/home/exp /root/exp":
           path => "/usr/bin/:/usr/sbin/:/usr/local/bin:/usr/local/sbin:/sbin/:/bin"
    }
}
node "ibr-1"{
	include ibrdtn_config
	include time_execute
	include pre_command
	include time_iptables
	include netem-agent_file
	include killagent_file
	include killdtn_file

    file { "/tmp/hosts2ports":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/hosts2ports"
    }


    file { "/tmp/cgr_l.1":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/cgr_l.1"
    }


    file { "/tmp/senders.1":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/senders.1"
    }


    file { "/tmp/receivers.1":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/receivers.1"
    }

	exec {'ifstat -i nsf635272d-20 >/root/exp/ibr/net/ibr-1.txt & netem-agent 1453702152.46 500 1 & ':
		path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:",
	}
}

node "ibr-2"{
	include ibrdtn_config
	include time_execute
	include pre_command
	include time_iptables
	include netem-agent_file
	include killagent_file
	include killdtn_file

    file { "/tmp/hosts2ports":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/hosts2ports"
    }


    file { "/tmp/cgr_l.2":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/cgr_l.2"
    }


    file { "/tmp/senders.2":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/senders.2"
    }


    file { "/tmp/receivers.2":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/receivers.2"
    }

	exec {'ifstat -i nsa14356f6-43 >/root/exp/ibr/net/ibr-2.txt & netem-agent 1453702152.46 500 1 & ':
		path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:",
	}
}

node "ibr-3"{
	include ibrdtn_config
	include time_execute
	include pre_command
	include time_iptables
	include netem-agent_file
	include killagent_file
	include killdtn_file

    file { "/tmp/hosts2ports":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/hosts2ports"
    }


    file { "/tmp/cgr_l.3":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/cgr_l.3"
    }


    file { "/tmp/senders.3":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/senders.3"
    }


    file { "/tmp/receivers.3":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/receivers.3"
    }

	exec {'ifstat -i ns0a22cd8a-06 >/root/exp/ibr/net/ibr-3.txt & netem-agent 1453702152.46 500 1 & ':
		path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:",
	}
}

node "ibr-4"{
	include ibrdtn_config
	include time_execute
	include pre_command
	include time_iptables
	include netem-agent_file
	include killagent_file
	include killdtn_file

    file { "/tmp/hosts2ports":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/hosts2ports"
    }


    file { "/tmp/cgr_l.4":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/cgr_l.4"
    }


    file { "/tmp/senders.4":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/senders.4"
    }


    file { "/tmp/receivers.4":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/receivers.4"
    }

	exec {'ifstat -i nsc2e20810-e9 >/root/exp/ibr/net/ibr-4.txt & netem-agent 1453702152.46 500 1 & ':
		path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:",
	}
}

node "ibr-5"{
	include ibrdtn_config
	include time_execute
	include pre_command
	include time_iptables
	include netem-agent_file
	include killagent_file
	include killdtn_file

    file { "/tmp/hosts2ports":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/hosts2ports"
    }


    file { "/tmp/cgr_l.5":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/cgr_l.5"
    }


    file { "/tmp/senders.5":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/senders.5"
    }


    file { "/tmp/receivers.5":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/receivers.5"
    }

	exec {'ifstat -i ns9d4b52cd-3a >/root/exp/ibr/net/ibr-5.txt & netem-agent 1453702152.46 500 1 & ':
		path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:",
	}
}

node "ibr-6"{
	include ibrdtn_config
	include time_execute
	include pre_command
	include time_iptables
	include netem-agent_file
	include killagent_file
	include killdtn_file

    file { "/tmp/hosts2ports":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/hosts2ports"
    }


    file { "/tmp/cgr_l.6":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/cgr_l.6"
    }


    file { "/tmp/senders.6":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/senders.6"
    }


    file { "/tmp/receivers.6":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/receivers.6"
    }

	exec {'ifstat -i ns6a50ff2f-a3 >/root/exp/ibr/net/ibr-6.txt & netem-agent 1453702152.46 500 1 & ':
		path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:",
	}
}

node "ibr-7"{
	include ibrdtn_config
	include time_execute
	include pre_command
	include time_iptables
	include netem-agent_file
	include killagent_file
	include killdtn_file

    file { "/tmp/hosts2ports":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/hosts2ports"
    }


    file { "/tmp/cgr_l.7":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/cgr_l.7"
    }


    file { "/tmp/senders.7":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/senders.7"
    }


    file { "/tmp/receivers.7":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/receivers.7"
    }

	exec {'ifstat -i ns19eab34f-7c >/root/exp/ibr/net/ibr-7.txt & netem-agent 1453702152.46 500 1 & ':
		path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:",
	}
}

node "ibr-8"{
	include ibrdtn_config
	include time_execute
	include pre_command
	include time_iptables
	include netem-agent_file
	include killagent_file
	include killdtn_file

    file { "/tmp/hosts2ports":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/hosts2ports"
    }


    file { "/tmp/cgr_l.8":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/cgr_l.8"
    }


    file { "/tmp/senders.8":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/senders.8"
    }


    file { "/tmp/receivers.8":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/receivers.8"
    }

	exec {'ifstat -i nsee551862-1b >/root/exp/ibr/net/ibr-8.txt & netem-agent 1453702152.46 500 1 & ':
		path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:",
	}
}

node "ibr-9"{
	include ibrdtn_config
	include time_execute
	include pre_command
	include time_iptables
	include netem-agent_file
	include killagent_file
	include killdtn_file

    file { "/tmp/hosts2ports":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/hosts2ports"
    }


    file { "/tmp/cgr_l.9":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/cgr_l.9"
    }


    file { "/tmp/senders.9":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/senders.9"
    }


    file { "/tmp/receivers.9":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/receivers.9"
    }

	exec {'ifstat -i nsd27a294a-da >/root/exp/ibr/net/ibr-9.txt & netem-agent 1453702152.46 500 1 & ':
		path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:",
	}
}

node "ibr-10"{
	include ibrdtn_config
	include time_execute
	include pre_command
	include time_iptables
	include netem-agent_file
	include killagent_file
	include killdtn_file

    file { "/tmp/hosts2ports":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/hosts2ports"
    }


    file { "/tmp/cgr_l.10":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/cgr_l.10"
    }


    file { "/tmp/senders.10":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/senders.10"
    }


    file { "/tmp/receivers.10":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/receivers.10"
    }

	exec {'ifstat -i nsf1721f15-84 >/root/exp/ibr/net/ibr-10.txt & netem-agent 1453702152.46 500 1 & ':
		path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:",
	}
}

node "ibr-11"{
	include ibrdtn_config
	include time_execute
	include pre_command
	include time_iptables
	include netem-agent_file
	include killagent_file
	include killdtn_file

    file { "/tmp/hosts2ports":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/hosts2ports"
    }


    file { "/tmp/cgr_l.11":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/cgr_l.11"
    }


    file { "/tmp/senders.11":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/senders.11"
    }


    file { "/tmp/receivers.11":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/receivers.11"
    }

	exec {'ifstat -i ns25e047c5-6e >/root/exp/ibr/net/ibr-11.txt & netem-agent 1453702152.46 500 1 & ':
		path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:",
	}
}

node "ibr-12"{
	include ibrdtn_config
	include time_execute
	include pre_command
	include time_iptables
	include netem-agent_file
	include killagent_file
	include killdtn_file

    file { "/tmp/hosts2ports":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/hosts2ports"
    }


    file { "/tmp/cgr_l.12":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/cgr_l.12"
    }


    file { "/tmp/senders.12":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/senders.12"
    }


    file { "/tmp/receivers.12":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/receivers.12"
    }

	exec {'ifstat -i ns5d45be90-7c >/root/exp/ibr/net/ibr-12.txt & netem-agent 1453702152.46 500 1 & ':
		path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:",
	}
}

node "ibr-13"{
	include ibrdtn_config
	include time_execute
	include pre_command
	include time_iptables
	include netem-agent_file
	include killagent_file
	include killdtn_file

    file { "/tmp/hosts2ports":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/hosts2ports"
    }


    file { "/tmp/cgr_l.13":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/cgr_l.13"
    }


    file { "/tmp/senders.13":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/senders.13"
    }


    file { "/tmp/receivers.13":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/receivers.13"
    }

	exec {'ifstat -i ns3a399589-1f >/root/exp/ibr/net/ibr-13.txt & netem-agent 1453702152.46 500 1 & ':
		path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:",
	}
}

node "ibr-14"{
	include ibrdtn_config
	include time_execute
	include pre_command
	include time_iptables
	include netem-agent_file
	include killagent_file
	include killdtn_file

    file { "/tmp/hosts2ports":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/hosts2ports"
    }


    file { "/tmp/cgr_l.14":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/cgr_l.14"
    }


    file { "/tmp/senders.14":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/senders.14"
    }


    file { "/tmp/receivers.14":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/receivers.14"
    }

	exec {'ifstat -i ns9980b105-92 >/root/exp/ibr/net/ibr-14.txt & netem-agent 1453702152.46 500 1 & ':
		path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:",
	}
}

node "ibr-15"{
	include ibrdtn_config
	include time_execute
	include pre_command
	include time_iptables
	include netem-agent_file
	include killagent_file
	include killdtn_file

    file { "/tmp/hosts2ports":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/hosts2ports"
    }


    file { "/tmp/cgr_l.15":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/cgr_l.15"
    }


    file { "/tmp/senders.15":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/senders.15"
    }


    file { "/tmp/receivers.15":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/receivers.15"
    }

	exec {'ifstat -i nsa953fae3-61 >/root/exp/ibr/net/ibr-15.txt & netem-agent 1453702152.46 500 1 & ':
		path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:",
	}
}

node "ibr-16"{
	include ibrdtn_config
	include time_execute
	include pre_command
	include time_iptables
	include netem-agent_file
	include killagent_file
	include killdtn_file

    file { "/tmp/hosts2ports":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/hosts2ports"
    }


    file { "/tmp/cgr_l.16":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/cgr_l.16"
    }


    file { "/tmp/senders.16":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/senders.16"
    }


    file { "/tmp/receivers.16":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/receivers.16"
    }

	exec {'ifstat -i nsc44ea41f-98 >/root/exp/ibr/net/ibr-16.txt & netem-agent 1453702152.46 500 1 & ':
		path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:",
	}
}

node "ibr-17"{
	include ibrdtn_config
	include time_execute
	include pre_command
	include time_iptables
	include netem-agent_file
	include killagent_file
	include killdtn_file

    file { "/tmp/hosts2ports":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/hosts2ports"
    }


    file { "/tmp/cgr_l.17":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/cgr_l.17"
    }


    file { "/tmp/senders.17":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/senders.17"
    }


    file { "/tmp/receivers.17":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/receivers.17"
    }

	exec {'ifstat -i ns046122d7-67 >/root/exp/ibr/net/ibr-17.txt & netem-agent 1453702152.46 500 1 & ':
		path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:",
	}
}

node "ibr-18"{
	include ibrdtn_config
	include time_execute
	include pre_command
	include time_iptables
	include netem-agent_file
	include killagent_file
	include killdtn_file

    file { "/tmp/hosts2ports":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/hosts2ports"
    }


    file { "/tmp/cgr_l.18":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/cgr_l.18"
    }


    file { "/tmp/senders.18":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/senders.18"
    }


    file { "/tmp/receivers.18":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/receivers.18"
    }

	exec {'ifstat -i ns8ee06544-d4 >/root/exp/ibr/net/ibr-18.txt & netem-agent 1453702152.46 500 1 & ':
		path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:",
	}
}

node "ibr-19"{
	include ibrdtn_config
	include time_execute
	include pre_command
	include time_iptables
	include netem-agent_file
	include killagent_file
	include killdtn_file

    file { "/tmp/hosts2ports":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/hosts2ports"
    }


    file { "/tmp/cgr_l.19":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/cgr_l.19"
    }


    file { "/tmp/senders.19":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/senders.19"
    }


    file { "/tmp/receivers.19":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/receivers.19"
    }

	exec {'ifstat -i ns9ee3fa0c-b4 >/root/exp/ibr/net/ibr-19.txt & netem-agent 1453702152.46 500 1 & ':
		path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:",
	}
}

node "ibr-20"{
	include ibrdtn_config
	include time_execute
	include pre_command
	include time_iptables
	include netem-agent_file
	include killagent_file
	include killdtn_file

    file { "/tmp/hosts2ports":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/hosts2ports"
    }


    file { "/tmp/cgr_l.20":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/cgr_l.20"
    }


    file { "/tmp/senders.20":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/senders.20"
    }


    file { "/tmp/receivers.20":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/receivers.20"
    }

	exec {'ifstat -i ns4bd44eba-5d >/root/exp/ibr/net/ibr-20.txt & netem-agent 1453702152.46 500 1 & ':
		path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:",
	}
}

node "ibr-21"{
	include ibrdtn_config
	include time_execute
	include pre_command
	include time_iptables
	include netem-agent_file
	include killagent_file
	include killdtn_file

    file { "/tmp/hosts2ports":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/hosts2ports"
    }


    file { "/tmp/cgr_l.21":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/cgr_l.21"
    }


    file { "/tmp/senders.21":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/senders.21"
    }


    file { "/tmp/receivers.21":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/receivers.21"
    }

	exec {'ifstat -i nsb021099a-3e >/root/exp/ibr/net/ibr-21.txt & netem-agent 1453702152.46 500 1 & ':
		path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:",
	}
}

node "ibr-22"{
	include ibrdtn_config
	include time_execute
	include pre_command
	include time_iptables
	include netem-agent_file
	include killagent_file
	include killdtn_file

    file { "/tmp/hosts2ports":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/hosts2ports"
    }


    file { "/tmp/cgr_l.22":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/cgr_l.22"
    }


    file { "/tmp/senders.22":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/senders.22"
    }


    file { "/tmp/receivers.22":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/receivers.22"
    }

	exec {'ifstat -i ns3371ef17-5b >/root/exp/ibr/net/ibr-22.txt & netem-agent 1453702152.46 500 1 & ':
		path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:",
	}
}

node "ibr-23"{
	include ibrdtn_config
	include time_execute
	include pre_command
	include time_iptables
	include netem-agent_file
	include killagent_file
	include killdtn_file

    file { "/tmp/hosts2ports":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/hosts2ports"
    }


    file { "/tmp/cgr_l.23":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/cgr_l.23"
    }


    file { "/tmp/senders.23":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/senders.23"
    }


    file { "/tmp/receivers.23":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/receivers.23"
    }

	exec {'ifstat -i ns068cae44-c9 >/root/exp/ibr/net/ibr-23.txt & netem-agent 1453702152.46 500 1 & ':
		path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:",
	}
}

node "ibr-24"{
	include ibrdtn_config
	include time_execute
	include pre_command
	include time_iptables
	include netem-agent_file
	include killagent_file
	include killdtn_file

    file { "/tmp/hosts2ports":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/hosts2ports"
    }


    file { "/tmp/cgr_l.24":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/cgr_l.24"
    }


    file { "/tmp/senders.24":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/senders.24"
    }


    file { "/tmp/receivers.24":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/receivers.24"
    }

	exec {'ifstat -i ns75cb2cd9-fd >/root/exp/ibr/net/ibr-24.txt & netem-agent 1453702152.46 500 1 & ':
		path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:",
	}
}

node "ibr-25"{
	include ibrdtn_config
	include time_execute
	include pre_command
	include time_iptables
	include netem-agent_file
	include killagent_file
	include killdtn_file

    file { "/tmp/hosts2ports":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/hosts2ports"
    }


    file { "/tmp/cgr_l.25":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/cgr_l.25"
    }


    file { "/tmp/senders.25":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/senders.25"
    }


    file { "/tmp/receivers.25":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/receivers.25"
    }

	exec {'ifstat -i nsf4035f67-38 >/root/exp/ibr/net/ibr-25.txt & netem-agent 1453702152.46 500 1 & ':
		path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:",
	}
}

node "ibr-26"{
	include ibrdtn_config
	include time_execute
	include pre_command
	include time_iptables
	include netem-agent_file
	include killagent_file
	include killdtn_file

    file { "/tmp/hosts2ports":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/hosts2ports"
    }


    file { "/tmp/cgr_l.26":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/cgr_l.26"
    }


    file { "/tmp/senders.26":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/senders.26"
    }


    file { "/tmp/receivers.26":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/receivers.26"
    }

	exec {'ifstat -i ns1e7ff9e7-62 >/root/exp/ibr/net/ibr-26.txt & netem-agent 1453702152.46 500 1 & ':
		path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:",
	}
}

node "ibr-27"{
	include ibrdtn_config
	include time_execute
	include pre_command
	include time_iptables
	include netem-agent_file
	include killagent_file
	include killdtn_file

    file { "/tmp/hosts2ports":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/hosts2ports"
    }


    file { "/tmp/cgr_l.27":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/cgr_l.27"
    }


    file { "/tmp/senders.27":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/senders.27"
    }


    file { "/tmp/receivers.27":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/receivers.27"
    }

	exec {'ifstat -i nsae9398d2-36 >/root/exp/ibr/net/ibr-27.txt & netem-agent 1453702152.46 500 1 & ':
		path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:",
	}
}

node "ibr-28"{
	include ibrdtn_config
	include time_execute
	include pre_command
	include time_iptables
	include netem-agent_file
	include killagent_file
	include killdtn_file

    file { "/tmp/hosts2ports":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/hosts2ports"
    }


    file { "/tmp/cgr_l.28":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/cgr_l.28"
    }


    file { "/tmp/senders.28":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/senders.28"
    }


    file { "/tmp/receivers.28":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/receivers.28"
    }

	exec {'ifstat -i ns29620a07-10 >/root/exp/ibr/net/ibr-28.txt & netem-agent 1453702152.46 500 1 & ':
		path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:",
	}
}

node "ibr-29"{
	include ibrdtn_config
	include time_execute
	include pre_command
	include time_iptables
	include netem-agent_file
	include killagent_file
	include killdtn_file

    file { "/tmp/hosts2ports":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/hosts2ports"
    }


    file { "/tmp/cgr_l.29":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/cgr_l.29"
    }


    file { "/tmp/senders.29":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/senders.29"
    }


    file { "/tmp/receivers.29":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/receivers.29"
    }

	exec {'ifstat -i ns9f8ef944-6d >/root/exp/ibr/net/ibr-29.txt & netem-agent 1453702152.46 500 1 & ':
		path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:",
	}
}

node "ibr-30"{
	include ibrdtn_config
	include time_execute
	include pre_command
	include time_iptables
	include netem-agent_file
	include killagent_file
	include killdtn_file

    file { "/tmp/hosts2ports":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/hosts2ports"
    }


    file { "/tmp/cgr_l.30":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/cgr_l.30"
    }


    file { "/tmp/senders.30":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/senders.30"
    }


    file { "/tmp/receivers.30":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/receivers.30"
    }

	exec {'ifstat -i ns1ff86fe4-9c >/root/exp/ibr/net/ibr-30.txt & netem-agent 1453702152.46 500 1 & ':
		path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:",
	}
}

node "ibr-31"{
	include ibrdtn_config
	include time_execute
	include pre_command
	include time_iptables
	include netem-agent_file
	include killagent_file
	include killdtn_file

    file { "/tmp/hosts2ports":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/hosts2ports"
    }


    file { "/tmp/cgr_l.31":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/cgr_l.31"
    }


    file { "/tmp/senders.31":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/senders.31"
    }


    file { "/tmp/receivers.31":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/receivers.31"
    }

	exec {'ifstat -i ns2ae9f255-8e >/root/exp/ibr/net/ibr-31.txt & netem-agent 1453702152.46 500 1 & ':
		path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:",
	}
}

node "ibr-32"{
	include ibrdtn_config
	include time_execute
	include pre_command
	include time_iptables
	include netem-agent_file
	include killagent_file
	include killdtn_file

    file { "/tmp/hosts2ports":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/hosts2ports"
    }


    file { "/tmp/cgr_l.32":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/cgr_l.32"
    }


    file { "/tmp/senders.32":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/senders.32"
    }


    file { "/tmp/receivers.32":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/receivers.32"
    }

	exec {'ifstat -i nsa09bbbaf-a5 >/root/exp/ibr/net/ibr-32.txt & netem-agent 1453702152.46 500 1 & ':
		path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:",
	}
}

node "ibr-33"{
	include ibrdtn_config
	include time_execute
	include pre_command
	include time_iptables
	include netem-agent_file
	include killagent_file
	include killdtn_file

    file { "/tmp/hosts2ports":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/hosts2ports"
    }


    file { "/tmp/cgr_l.33":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/cgr_l.33"
    }


    file { "/tmp/senders.33":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/senders.33"
    }


    file { "/tmp/receivers.33":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/receivers.33"
    }

	exec {'ifstat -i nsd32839d3-7c >/root/exp/ibr/net/ibr-33.txt & netem-agent 1453702152.46 500 1 & ':
		path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:",
	}
}

node "ibr-34"{
	include ibrdtn_config
	include time_execute
	include pre_command
	include time_iptables
	include netem-agent_file
	include killagent_file
	include killdtn_file

    file { "/tmp/hosts2ports":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/hosts2ports"
    }


    file { "/tmp/cgr_l.34":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/cgr_l.34"
    }


    file { "/tmp/senders.34":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/senders.34"
    }


    file { "/tmp/receivers.34":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/receivers.34"
    }

	exec {'ifstat -i ns0b0fff8b-f2 >/root/exp/ibr/net/ibr-34.txt & netem-agent 1453702152.46 500 1 & ':
		path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:",
	}
}

node "ibr-35"{
	include ibrdtn_config
	include time_execute
	include pre_command
	include time_iptables
	include netem-agent_file
	include killagent_file
	include killdtn_file

    file { "/tmp/hosts2ports":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/hosts2ports"
    }


    file { "/tmp/cgr_l.35":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/cgr_l.35"
    }


    file { "/tmp/senders.35":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/senders.35"
    }


    file { "/tmp/receivers.35":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/receivers.35"
    }

	exec {'ifstat -i nsdb413f61-d1 >/root/exp/ibr/net/ibr-35.txt & netem-agent 1453702152.46 500 1 & ':
		path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:",
	}
}

node "ibr-36"{
	include ibrdtn_config
	include time_execute
	include pre_command
	include time_iptables
	include netem-agent_file
	include killagent_file
	include killdtn_file

    file { "/tmp/hosts2ports":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/hosts2ports"
    }


    file { "/tmp/cgr_l.36":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/cgr_l.36"
    }


    file { "/tmp/senders.36":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/senders.36"
    }


    file { "/tmp/receivers.36":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/receivers.36"
    }

	exec {'ifstat -i nse323a616-d7 >/root/exp/ibr/net/ibr-36.txt & netem-agent 1453702152.46 500 1 & ':
		path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:",
	}
}

node "ibr-37"{
	include ibrdtn_config
	include time_execute
	include pre_command
	include time_iptables
	include netem-agent_file
	include killagent_file
	include killdtn_file

    file { "/tmp/hosts2ports":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/hosts2ports"
    }


    file { "/tmp/cgr_l.37":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/cgr_l.37"
    }


    file { "/tmp/senders.37":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/senders.37"
    }


    file { "/tmp/receivers.37":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/receivers.37"
    }

	exec {'ifstat -i ns5ea73d82-7e >/root/exp/ibr/net/ibr-37.txt & netem-agent 1453702152.46 500 1 & ':
		path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:",
	}
}

node "ibr-38"{
	include ibrdtn_config
	include time_execute
	include pre_command
	include time_iptables
	include netem-agent_file
	include killagent_file
	include killdtn_file

    file { "/tmp/hosts2ports":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/hosts2ports"
    }


    file { "/tmp/cgr_l.38":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/cgr_l.38"
    }


    file { "/tmp/senders.38":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/senders.38"
    }


    file { "/tmp/receivers.38":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/receivers.38"
    }

	exec {'ifstat -i nsfad76d56-39 >/root/exp/ibr/net/ibr-38.txt & netem-agent 1453702152.46 500 1 & ':
		path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:",
	}
}

node "ibr-39"{
	include ibrdtn_config
	include time_execute
	include pre_command
	include time_iptables
	include netem-agent_file
	include killagent_file
	include killdtn_file

    file { "/tmp/hosts2ports":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/hosts2ports"
    }


    file { "/tmp/cgr_l.39":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/cgr_l.39"
    }


    file { "/tmp/senders.39":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/senders.39"
    }


    file { "/tmp/receivers.39":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/receivers.39"
    }

	exec {'ifstat -i nsc5a66d82-31 >/root/exp/ibr/net/ibr-39.txt & netem-agent 1453702152.46 500 1 & ':
		path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:",
	}
}

node "ibr-40"{
	include ibrdtn_config
	include time_execute
	include pre_command
	include time_iptables
	include netem-agent_file
	include killagent_file
	include killdtn_file

    file { "/tmp/hosts2ports":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/hosts2ports"
    }


    file { "/tmp/cgr_l.40":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/cgr_l.40"
    }


    file { "/tmp/senders.40":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/senders.40"
    }


    file { "/tmp/receivers.40":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/receivers.40"
    }

	exec {'ifstat -i ns57ffebad-c8 >/root/exp/ibr/net/ibr-40.txt & netem-agent 1453702152.46 500 1 & ':
		path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:",
	}
}

node "ibr-41"{
	include ibrdtn_config
	include time_execute
	include pre_command
	include time_iptables
	include netem-agent_file
	include killagent_file
	include killdtn_file

    file { "/tmp/hosts2ports":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/hosts2ports"
    }


    file { "/tmp/cgr_l.41":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/cgr_l.41"
    }


    file { "/tmp/senders.41":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/senders.41"
    }


    file { "/tmp/receivers.41":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/receivers.41"
    }

	exec {'ifstat -i ns689419b5-f9 >/root/exp/ibr/net/ibr-41.txt & netem-agent 1453702152.46 500 1 & ':
		path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:",
	}
}

node "ibr-42"{
	include ibrdtn_config
	include time_execute
	include pre_command
	include time_iptables
	include netem-agent_file
	include killagent_file
	include killdtn_file

    file { "/tmp/hosts2ports":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/hosts2ports"
    }


    file { "/tmp/cgr_l.42":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/cgr_l.42"
    }


    file { "/tmp/senders.42":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/senders.42"
    }


    file { "/tmp/receivers.42":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/receivers.42"
    }

	exec {'ifstat -i ns6013eb4e-20 >/root/exp/ibr/net/ibr-42.txt & netem-agent 1453702152.46 500 1 & ':
		path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:",
	}
}

node "ibr-43"{
	include ibrdtn_config
	include time_execute
	include pre_command
	include time_iptables
	include netem-agent_file
	include killagent_file
	include killdtn_file

    file { "/tmp/hosts2ports":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/hosts2ports"
    }


    file { "/tmp/cgr_l.43":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/cgr_l.43"
    }


    file { "/tmp/senders.43":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/senders.43"
    }


    file { "/tmp/receivers.43":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/receivers.43"
    }

	exec {'ifstat -i nsfb3cf61a-74 >/root/exp/ibr/net/ibr-43.txt & netem-agent 1453702152.46 500 1 & ':
		path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:",
	}
}

node "ibr-44"{
	include ibrdtn_config
	include time_execute
	include pre_command
	include time_iptables
	include netem-agent_file
	include killagent_file
	include killdtn_file

    file { "/tmp/hosts2ports":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/hosts2ports"
    }


    file { "/tmp/cgr_l.44":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/cgr_l.44"
    }


    file { "/tmp/senders.44":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/senders.44"
    }


    file { "/tmp/receivers.44":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/receivers.44"
    }

	exec {'ifstat -i ns46e747d7-05 >/root/exp/ibr/net/ibr-44.txt & netem-agent 1453702152.46 500 1 & ':
		path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:",
	}
}

node "ibr-45"{
	include ibrdtn_config
	include time_execute
	include pre_command
	include time_iptables
	include netem-agent_file
	include killagent_file
	include killdtn_file

    file { "/tmp/hosts2ports":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/hosts2ports"
    }


    file { "/tmp/cgr_l.45":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/cgr_l.45"
    }


    file { "/tmp/senders.45":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/senders.45"
    }


    file { "/tmp/receivers.45":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/receivers.45"
    }

	exec {'ifstat -i ns188ba360-9f >/root/exp/ibr/net/ibr-45.txt & netem-agent 1453702152.46 500 1 & ':
		path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:",
	}
}

node "ibr-46"{
	include ibrdtn_config
	include time_execute
	include pre_command
	include time_iptables
	include netem-agent_file
	include killagent_file
	include killdtn_file

    file { "/tmp/hosts2ports":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/hosts2ports"
    }


    file { "/tmp/cgr_l.46":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/cgr_l.46"
    }


    file { "/tmp/senders.46":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/senders.46"
    }


    file { "/tmp/receivers.46":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/receivers.46"
    }

	exec {'ifstat -i ns4a36e38c-67 >/root/exp/ibr/net/ibr-46.txt & netem-agent 1453702152.46 500 1 & ':
		path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:",
	}
}

node "ibr-47"{
	include ibrdtn_config
	include time_execute
	include pre_command
	include time_iptables
	include netem-agent_file
	include killagent_file
	include killdtn_file

    file { "/tmp/hosts2ports":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/hosts2ports"
    }


    file { "/tmp/cgr_l.47":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/cgr_l.47"
    }


    file { "/tmp/senders.47":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/senders.47"
    }


    file { "/tmp/receivers.47":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/receivers.47"
    }

	exec {'ifstat -i nsda34fa78-54 >/root/exp/ibr/net/ibr-47.txt & netem-agent 1453702152.46 500 1 & ':
		path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:",
	}
}

node "ibr-48"{
	include ibrdtn_config
	include time_execute
	include pre_command
	include time_iptables
	include netem-agent_file
	include killagent_file
	include killdtn_file

    file { "/tmp/hosts2ports":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/hosts2ports"
    }


    file { "/tmp/cgr_l.48":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/cgr_l.48"
    }


    file { "/tmp/senders.48":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/senders.48"
    }


    file { "/tmp/receivers.48":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/receivers.48"
    }

	exec {'ifstat -i ns11c31212-af >/root/exp/ibr/net/ibr-48.txt & netem-agent 1453702152.46 500 1 & ':
		path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:",
	}
}

node "ibr-49"{
	include ibrdtn_config
	include time_execute
	include pre_command
	include time_iptables
	include netem-agent_file
	include killagent_file
	include killdtn_file

    file { "/tmp/hosts2ports":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/hosts2ports"
    }


    file { "/tmp/cgr_l.49":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/cgr_l.49"
    }


    file { "/tmp/senders.49":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/senders.49"
    }


    file { "/tmp/receivers.49":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/receivers.49"
    }

	exec {'ifstat -i ns199f4fca-93 >/root/exp/ibr/net/ibr-49.txt & netem-agent 1453702152.46 500 1 & ':
		path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:",
	}
}

node "ibr-50"{
	include ibrdtn_config
	include time_execute
	include pre_command
	include time_iptables
	include netem-agent_file
	include killagent_file
	include killdtn_file

    file { "/tmp/hosts2ports":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/hosts2ports"
    }


    file { "/tmp/cgr_l.50":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/cgr_l.50"
    }


    file { "/tmp/senders.50":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/senders.50"
    }


    file { "/tmp/receivers.50":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/receivers.50"
    }

	exec {'ifstat -i ns23456d73-68 >/root/exp/ibr/net/ibr-50.txt & netem-agent 1453702152.46 500 1 & ':
		path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:",
	}
}

node "ibr-51"{
	include ibrdtn_config
	include time_execute
	include pre_command
	include time_iptables
	include netem-agent_file
	include killagent_file
	include killdtn_file

    file { "/tmp/hosts2ports":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/hosts2ports"
    }


    file { "/tmp/cgr_l.51":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/cgr_l.51"
    }


    file { "/tmp/senders.51":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/senders.51"
    }


    file { "/tmp/receivers.51":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/receivers.51"
    }

	exec {'ifstat -i ns96ace31e-08 >/root/exp/ibr/net/ibr-51.txt & netem-agent 1453702152.46 500 1 & ':
		path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:",
	}
}

node "ibr-52"{
	include ibrdtn_config
	include time_execute
	include pre_command
	include time_iptables
	include netem-agent_file
	include killagent_file
	include killdtn_file

    file { "/tmp/hosts2ports":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/hosts2ports"
    }


    file { "/tmp/cgr_l.52":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/cgr_l.52"
    }


    file { "/tmp/senders.52":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/senders.52"
    }


    file { "/tmp/receivers.52":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/receivers.52"
    }

	exec {'ifstat -i ns3fcafe90-b2 >/root/exp/ibr/net/ibr-52.txt & netem-agent 1453702152.46 500 1 & ':
		path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:",
	}
}

node "ibr-53"{
	include ibrdtn_config
	include time_execute
	include pre_command
	include time_iptables
	include netem-agent_file
	include killagent_file
	include killdtn_file

    file { "/tmp/hosts2ports":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/hosts2ports"
    }


    file { "/tmp/cgr_l.53":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/cgr_l.53"
    }


    file { "/tmp/senders.53":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/senders.53"
    }


    file { "/tmp/receivers.53":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/receivers.53"
    }

	exec {'ifstat -i nsaec33de6-91 >/root/exp/ibr/net/ibr-53.txt & netem-agent 1453702152.46 500 1 & ':
		path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:",
	}
}

node "ibr-54"{
	include ibrdtn_config
	include time_execute
	include pre_command
	include time_iptables
	include netem-agent_file
	include killagent_file
	include killdtn_file

    file { "/tmp/hosts2ports":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/hosts2ports"
    }


    file { "/tmp/cgr_l.54":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/cgr_l.54"
    }


    file { "/tmp/senders.54":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/senders.54"
    }


    file { "/tmp/receivers.54":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/receivers.54"
    }

	exec {'ifstat -i nsf7e4be2d-85 >/root/exp/ibr/net/ibr-54.txt & netem-agent 1453702152.46 500 1 & ':
		path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:",
	}
}

node "ibr-55"{
	include ibrdtn_config
	include time_execute
	include pre_command
	include time_iptables
	include netem-agent_file
	include killagent_file
	include killdtn_file

    file { "/tmp/hosts2ports":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/hosts2ports"
    }


    file { "/tmp/cgr_l.55":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/cgr_l.55"
    }


    file { "/tmp/senders.55":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/senders.55"
    }


    file { "/tmp/receivers.55":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/receivers.55"
    }

	exec {'ifstat -i nsf556936c-f6 >/root/exp/ibr/net/ibr-55.txt & netem-agent 1453702152.46 500 1 & ':
		path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:",
	}
}

node "ibr-56"{
	include ibrdtn_config
	include time_execute
	include pre_command
	include time_iptables
	include netem-agent_file
	include killagent_file
	include killdtn_file

    file { "/tmp/hosts2ports":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/hosts2ports"
    }


    file { "/tmp/cgr_l.56":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/cgr_l.56"
    }


    file { "/tmp/senders.56":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/senders.56"
    }


    file { "/tmp/receivers.56":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/receivers.56"
    }

	exec {'ifstat -i ns685aa49a-b5 >/root/exp/ibr/net/ibr-56.txt & netem-agent 1453702152.46 500 1 & ':
		path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:",
	}
}

