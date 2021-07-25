module {{sender}}::MyLegacy {
	use 0x1::Signer;
	use 0x1::Timestamp;
	use 0x1::Errors;
	use 0x1::Vector;
	use 0x1::Account;
	use 0x1::Token::Token;
	use 0x1::STC::STC;

	struct Payment has key, store {
		id: u64,
		value: u64,
		balance: Token<STC>,
		time_lock: u64,
	}

    fun new_payment(account: &signer, id:u64, value:u64, time_lock:u64): Payment {
		Payment{id, value, balance: Account::withdraw(account, (value as u128)), time_lock}
    }

	struct Legacy has key, store {
		payer: address,
		payee: address,

		total_value:u64,
		times:u64,
		freq:u64,

		unpaid: vector<Payment>,
	}

    /// An offer of the specified type for the account does not match
    const EOFFER_DNE_FOR_ACCOUNT: u64 = 101;

    fun new_legacy(account: &signer, payee: address, total_value:u64, times:u64, freq:u64): Legacy {
		let value_each_payment = total_value / times;
		let now = Timestamp::now_seconds();

		let payments = Vector::empty<Payment>();
		let id = 0;
		while (id < times) {
			Vector::push_back(
				&mut payments, 
				new_payment(account, id, value_each_payment, now + id * freq)
			);
			id = id + 1;
		};

		let legacy = Legacy {
			payer: Signer::address_of(account),
			payee,

			total_value,
			times,
			freq,

			unpaid: payments,
		};

		legacy
    }

    fun init(account: &signer, payee: address, total_value: u64, times: u64, freq: u64) {
    	move_to(account, new_legacy(account, payee, total_value, times, freq));
    }

	fun redeem_id(account: &signer, legacy: &mut Legacy, id: u64) {
		let i = 0;
		while (i < Vector::length(&legacy.unpaid)) {
			if (Vector::borrow(&legacy.unpaid, i).id == id) {
				let Payment {id: _, value: _, balance, time_lock: _} = Vector::remove<Payment>(
					&mut legacy.unpaid, i);
		
				Account::deposit_to_self<STC>(account, balance);
				break
			};
			i = i + 1;
		}
	}
	
    fun redeem_once(account: signer, payer: address) acquires Legacy {
		let payee: address = Signer::address_of(&account);

		let legacy = borrow_global_mut<Legacy>(payer);

		assert(
			legacy.payee == payee || legacy.payer == payee, 
			Errors::invalid_argument(EOFFER_DNE_FOR_ACCOUNT)
		);

		let now = Timestamp::now_seconds();
		let redeemable_ids = Vector::empty<u64>();
		let i = 0;
		while (i < Vector::length(&legacy.unpaid)) {
			let payment = Vector::borrow(&legacy.unpaid, i);
			if (payment.time_lock < now) {
				Vector::push_back(&mut redeemable_ids, payment.id);
			};
			i = i + 1;
		};

		while (Vector::length(&redeemable_ids) > 0) {
			let id = Vector::pop_back<u64>(&mut redeemable_ids);
			Self::redeem_id(&account, legacy, id);
		}
    }

    public(script) fun init_legacy(account: signer, payee: address, total_value: u64, times: u64, freq: u64) {
    	Self::init(&account, payee, total_value, times, freq)
    }

    public(script) fun redeem(account: signer, payer: address) acquires Legacy {
    	Self::redeem_once(account, payer)
    }
}
