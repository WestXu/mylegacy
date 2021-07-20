module {{sender}}::MyInstallments {
	use 0x1::Signer;
	use 0x1::Vector;
	use 0x1::TransferScripts::peer_to_peer_v2;

	struct Payment has key, store {
		id: u64,
		value: u64,
	}

    public fun new_payment(id:u64, value:u64): Payment {
		Payment{id, value}
    }

	public fun get_payment_value(payment: &Payment): u64 {
		payment.value
	}

	struct Installments has key, store {
		payee: address,

		total_value:u64,
		times:u64,

		unpaid: vector<Payment>,
		paid: vector<Payment>,
	}

    public fun new_installments(payee: address, total_value:u64, times:u64): Installments {
		let value_each_payment = total_value / times;

		let payments = Vector::empty<Payment>();
		let id = 0;
		while (id < times) {
			Vector::push_back(&mut payments, new_payment(id, value_each_payment));
			id = id + 1;
		};

		let installments = Installments {
			payee,

			total_value,
			times,

			unpaid: payments,
			paid: Vector::empty<Payment>()
		};

		installments
    }

    public fun init(account: &signer, payee: address, total_value: u64, times: u64) {
    	move_to(account, new_installments(payee, total_value, times));
    }
	
    public(script) fun pay_once(account: signer) acquires Installments {
		let installments = borrow_global_mut<Installments>(Signer::address_of(&account));

		let payment = Vector::pop_back<Payment>(&mut installments.unpaid);

		peer_to_peer_v2<0x1::STC::STC>(account, installments.payee, (get_payment_value(&payment) as u128));

		Vector::push_back(&mut installments.paid, payment);
    }

    public(script) fun init_installments(account: signer, payee: address, total_value: u64, times: u64) {
    	Self::init(&account, payee, total_value, times)
    }

    public(script) fun pay(account: signer) acquires Installments {
    	Self::pay_once(account)
    }
}
