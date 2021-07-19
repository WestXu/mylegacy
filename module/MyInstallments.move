module {{sender}}::MyInstallments {
	use 0x1::Signer;
	use 0x1::Vector;

	struct Payment has key, store {
		id: u64,
		value: u64,
	}

	struct Installments has key, store {
		total_value:u64,
		times:u64,

		unpaid: vector<Payment>,
		paid: vector<Payment>,
	}

    public fun new_installments(total_value:u64, times:u64): Installments {
		let value_each_payment = total_value / times;

		let payments = Vector::empty<Payment>();
		let id = 0;
		while (id < times) {
			Vector::push_back(&mut payments, Payment{id, value: value_each_payment});
			id = id + 1;
		};

		let installments = Installments {
			total_value,
			times,

			unpaid: payments,
			paid: Vector::empty<Payment>()
		};

		installments
    }

    public fun init(account: &signer, total_value: u64, times: u64) {
    	move_to(account, new_installments(total_value, times));
    }
	
    public fun pay_once(account: &signer) acquires Installments {
		let installments = borrow_global_mut<Installments>(Signer::address_of(account));

		Vector::push_back(
			&mut installments.paid,
			Vector::pop_back<Payment>(&mut installments.unpaid)
		);
    }

    public(script) fun init_installments(account: signer, total_value: u64, times: u64) {
    	Self::init(&account, total_value, times)
    }

    public(script) fun pay(account: signer) acquires Installments {
    	Self::pay_once(&account)
    }
}
