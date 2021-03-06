import { arrayify, hexlify } from '@ethersproject/bytes'
import BigNumber from 'bignumber.js'
import { providers, utils, bcs } from '@starcoin/starcoin'

const contract_address = "0xe11eA1971774192FD96bA7FCA842128F"

window.show_alert = (is_success, html_msg, alert_id) => {
  const alert = document.getElementById(alert_id)
  alert.className = `alert alert-${is_success ? "success" : "danger"} fade show`
  alert.innerHTML = html_msg
}

window.initialize = async (alert_id) => {
  console.log('initialize')
  try {
    // We must specify the network as 'any' for starcoin to allow network changes
    window.starcoinProvider = new providers.Web3Provider(window.starcoin, 'any')
  } catch (error) {
    window.show_alert(false, ("Error: Couldn't find StarMask. " +
      `<a href="https://github.com/starcoinorg/starmask-extension" target="_blank">Install.</a>`), alert_id)
    throw error
  }
}

window.connect = async (alert_id) => {
  try {
    await window.starcoin.request({
      method: 'stc_requestAccounts',
    })
  } catch (error) {
    window.show_alert(false, `Error: ${error.message}`, alert_id)
    throw error
  }
}

window.send_transaction = async (payloadInHex, alert_id) => {
  try {
    console.log({ payloadInHex })

    const transactionHash = await window.starcoinProvider.getSigner().sendUncheckedTransaction({
      data: payloadInHex,
    })
    console.log({ transactionHash })

    window.show_alert(true, ("Successfully submitted your transaction. " +
      `<a href="https://staratlas.vercel.app/${window.starcoinProvider.network.name}/tx/${transactionHash}" target="_blank">Check it out.</a>`), alert_id)


  } catch (error) {
    window.show_alert(false, `Error: ${error.message}`, alert_id)
    throw error
  }
}

function asNano(amountStr) {
  const BIG_NUMBER_NANO_STC_MULTIPLIER = new BigNumber('1000000000')
  const sendAmountSTC = new BigNumber(String(amountStr), 10)
  const sendAmountNanoSTC = sendAmountSTC.times(BIG_NUMBER_NANO_STC_MULTIPLIER)
  return sendAmountNanoSTC
}

function asSCSHex(amount) {
  const se = new bcs.BcsSerializer()
  se.serializeU64(BigInt(amount.toString(10)))
  return hexlify(se.getBytes())
}

function amountAsSCSHex(amountStr) {
  const sendAmountNanoSTC = asNano(amountStr)
  const amountSCSHex = asSCSHex(sendAmountNanoSTC)
  return amountSCSHex
}

function getPayloadInHex(functionId, rawArgs, strTypeArgs) {
  const tyArgs = utils.tx.encodeStructTypeTags(strTypeArgs)
  const args = rawArgs.map(arrayify)

  const payloadInHex = (function () {
    const se = new bcs.BcsSerializer()
    const scriptFunction = utils.tx.encodeScriptFunction(functionId, tyArgs, args)
    scriptFunction.serialize(se)
    return hexlify(se.getBytes())
  })()

  return payloadInHex
}

function transfer() {
  // as demo
  getPayloadInHex(
    '0x1::TransferScripts::peer_to_peer_v2',
    [
      document.getElementById('toAccountInput').value,
      amountAsSCSHex(document.getElementById('amountInput').value)
    ],
    ['0x1::STC::STC']
  )
}


document.getElementById("redeem-button").onclick = async () => {
  await window.initialize('redeem-alert')
  await window.connect('redeem-alert')
  await window.send_transaction(
    getPayloadInHex(
      `${contract_address}::MyLegacy::redeem`,
      [
        document.getElementById('redeem-payer_address').value,
      ],
      []
    ),
    'redeem-alert'
  )
}

document.getElementById("init_legacy-button").onclick = async () => {
  await window.initialize('init_legacy-alert')
  await window.connect('init_legacy-alert')
  await window.send_transaction(
    getPayloadInHex(
      `${contract_address}::MyLegacy::init_legacy`,
      [
        document.getElementById('init_legacy-payee_address').value,
        amountAsSCSHex(document.getElementById('init_legacy-total_value').value),
        asSCSHex(document.getElementById('init_legacy-times').value),
        asSCSHex(
          parseInt(document.getElementById('init_legacy-freq_num').value)
          * new Map([
            ['1', 60 * 60 * 24 * 365],  // Years
            ['2', 60 * 60 * 24 * 30],  // Months
            ['3', 60 * 60 * 24],  // Days
            ['4', 60 * 60],  // Hours
            ['5', 60],  // Minutes
            ['6', 1],  // Seconds
          ]).get(
            document.getElementById('init_legacy-freq_unit').value
          )
        )
      ],
      []
    ),
    'init_legacy-alert'
  )
}
