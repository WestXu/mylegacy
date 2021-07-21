module {{sender}}::MyLegacy {
	use 0x1::Signer;
	use 0x1::Errors;
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

	struct Legacy has key, store {
		payer: address,
		payee: address,

		total_value:u64,
		times:u64,

		unpaid: vector<Payment>,
	}

    /// An offer of the specified type for the account does not match
    const EOFFER_DNE_FOR_ACCOUNT: u64 = 101;

    public fun new_legacy(account: &signer, payee: address, total_value:u64, times:u64): Legacy {
		let value_each_payment = total_value / times;

		let payments = Vector::empty<Payment>();
		let id = 0;
		while (id < times) {
			Vector::push_back(&mut payments, new_payment(account, id, value_each_payment));
			id = id + 1;
		};

		let legacy = Legacy {
			payer: Signer::address_of(account),
			payee,

			total_value,
			times,

			unpaid: payments,
		};

		legacy
    }

    public fun init(account: &signer, payee: address, total_value: u64, times: u64) {
    	move_to(account, new_legacy(account, payee, total_value, times));
    }
	
    public(script) fun redeem_once(account: signer, payer: address) acquires Legacy {
		let payee: address = Signer::address_of(&account);

		let legacy = borrow_global_mut<Legacy>(payer);

		assert(
			legacy.payee == payee || legacy.payee == payer, 
			Errors::invalid_argument(EOFFER_DNE_FOR_ACCOUNT)
		);

		let Payment {id: _, value: _, balance} = Vector::pop_back<Payment>(&mut legacy.unpaid);

		Account::deposit_to_self<STC>(&account, balance);
    }

    public(script) fun init_legacy(account: signer, payee: address, total_value: u64, times: u64) {
    	Self::init(&account, payee, total_value, times)
    }

    public(script) fun redeem(account: signer, payer: address) acquires Legacy {
    	Self::redeem_once(account, payer)
    }
}
