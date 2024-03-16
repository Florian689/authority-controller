# Authority-Controller Application Setup Guide

This document outlines the setup process for the 'authority-controller' application. The application is developed as part of the Bachelor's thesis titled "Secure Ballots: Authentication and Anonymity in Online Elections through SSI" by Florian Wehner at the Department of Service-centric Networking at TU Berlin.The authority-controller serves as a pilot proposal for an online process tailored to the German Bundestag Election, utilizing Self-Sovereign Identity (SSI) principles. Ideally, in a real-life scenario, it would be hosted by German Local Authorities. The authority-controller enhances the registration process for the online election by verifying the identity and eligibility of voters. It acts as a controller for an AcaPy instance, issuing Digital Polling Cards as Verifiable Credentials to eligible citizens.

The following software must be installed on your machine:
    - Python
    - Docker and Docker-compose
    - Ngrok
    - JQ

**1. Start ngrok** from a new terminal running `ngrok http 8020`

**2. Register DID** on the BCLedger at `http://test.bcovrin.vonx.io/` using a 32bit wallet seed. Remember your seed, we need it to start the AcaPy agent. Attention: The seed should not have been used before by another instance of AcaPy, because this can lead to synchronizing problems between the ledger and the agent.

**3. Start AcaPy Agent**
     **3.1 Exchange the <ngrok_endpoint>** in the command below with the endpoint shown in the ngrok terminal (e.g.: `https://7f7c-34-16-203-117.ngrok-free.app`).
     **3.2 Exchange the <seed>** with the 32bit-seed that you registered on the ledger.
     **3.3 Start an instance of the AcaPy Agent** from the auries-cloudagent-python root directory running the following command:

`PORTS="8020:8020 8021:8021" EVENTS=1 scripts/run_docker start --endpoint <ngrok_endpoint> --label authority.agent --auto-ping-connection --auto-respond-messages --inbound-transport http 0.0.0.0 8020 --outbound-transport http --admin 0.0.0.0 8021 --admin-insecure-mode --genesis-url http://test.bcovrin.vonx.io/genesis --wallet-type askar --wallet-name authority.agent744140 --wallet-key authority.agent744140 --preserve-exchange-record --auto-provision --public-invites --seed <seed> --webhook-url http://172.17.0.1:8000/webhook --monitor-revocation-notification --trace-target log --trace-tag acapy.events --trace-label authority.agent.trace --auto-accept-invites --auto-accept-requests --auto-store-credential`

**4. Build and start Authority Controller** from the authority-controller root directory running `docker-compose up --build` on Mac or `docker compose up --build` on Linux

**5. Start Registration Process** by visiting `http://localhost:8000` in your browser.

**6. Use the BC Wallet** to scan the QR-Code on the Registration Website and to be able to receive the polling card VC