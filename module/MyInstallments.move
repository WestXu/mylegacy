module {{sender}}::MyInstallments {
	use 0x1::Vector;
	use 0x1::Account;
	use 0x1::Token::Token;
	use 0x1::STC::STC;

	struct Payment has key, store {
		id: u64,
		value: u64,
		balance: Token<STC>,
	}

    public fun new_payment(account: &signer, id:u64, value:u64): Payment {
		Payment{id, value, balance: Account::withdraw(account, (value as u128))}
    }

	struct Installments has key, store {
		payee: address,

		total_value:u64,
		times:u64,

		unpaid: vector<Payment>,
	}

    public fun new_installments(account: &signer, payee: address, total_value:u64, times:u64): Installments {
		let value_each_payment = total_value / times;

		let payments = Vector::empty<Payment>();
		let id = 0;
		while (id < times) {
			Vector::push_back(&mut payments, new_payment(account, id, value_each_payment));
			id = id + 1;
		};

		let installments = Installments {
			payee,

			total_value,
			times,

			unpaid: payments,
		};

		installments
    }

    public fun init(account: &signer, payee: address, total_value: u64, times: u64) {
    	move_to(account, new_installments(account, payee, total_value, times));
    }
	
    public(script) fun redeem_once(account: signer) acquires Installments {
		let sender_address: address = @{{sender}};

		let installments = borrow_global_mut<Installments>(sender_address);

		let Payment {id: _, value: _, balance} = Vector::pop_back<Payment>(&mut installments.unpaid);

		Account::deposit_to_self<STC>(&account, balance);
    }

    public(script) fun init_installments(account: signer, payee: address, total_value: u64, times: u64) {
    	Self::init(&account, payee, total_value, times)
    }

    public(script) fun redeem(account: signer) acquires Installments {
    	Self::redeem_once(account)
    }
}
