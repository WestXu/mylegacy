import { arrayify, hexlify } from '@ethersproject/bytes'
import BigNumber from 'bignumber.js'
import StarMaskOnboarding from '@starcoin/starmask-onboarding'
import { providers, utils, bcs, encoding } from '@starcoin/starcoin'

let starcoinProvider

const currentUrl = new URL(window.location.href)
const forwarderOrigin = currentUrl.hostname === 'localhost'
  ? 'http://localhost:9032'
  : undefined

const { isStarMaskInstalled } = StarMaskOnboarding

window.initialize = async () => {
  console.log('initialize')
  try {
    if (window.starcoin) {
      // We must specify the network as 'any' for starcoin to allow network changes
      window.starcoinProvider = new providers.Web3Provider(window.starcoin, 'any')
    }
  } catch (error) {
    console.error(error)
  }
}

window.connect = async () => {
  try {
    const newAccounts = await window.starcoin.request({
      method: 'stc_requestAccounts',
    })
    // handleNewAccounts(newAccounts)
  } catch (error) {
    console.error(error)
  }
}

window.send_transaction = async (payloadInHex, alert_id) => {
  const alert = document.getElementById(alert_id)

  try {
    console.log({ payloadInHex })

    const transactionHash = await window.starcoinProvider.getSigner().sendUncheckedTransaction({
      data: payloadInHex,
    })
    console.log({ transactionHash })
    alert.className = "alert alert-success fade show"
    alert.innerHTML = `Successfully submitted your transaction. Check it out at https://stcscan.io/main/transactions/detail/${transactionHash}`

  } catch (error) {
    console.error({ error })
    alert.className = "alert alert-danger fade show"
    alert.innerHTML = `Error: ${error.message}`
  }
}
