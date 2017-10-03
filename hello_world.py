#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    hello world for symphony
'''

__author__ = 'Symphony LLC'
__email__ = 'email@symphony.com'
__copyright__ = 'Copyright 2017, Symphony'

import symphony
#import json
import requests


def main():
    
    ''' main program loop '''
    conn = symphony.Config('es-bot.cfg')
    # connect to pod
    try:
        agent, pod, symphony_sid, ifttt_webhook = conn.connect()
        print 'connected: %s' % symphony_sid
        print agent
        print pod
        #print session_token
    except Exception as err:
        #print 'failed to connect!'
        print err

    statcode, id = agent.create_datafeed()
    print('create datafeed status code: ')
    print(statcode)
    print('create datafeed id')
    print(id)    
    while 1:
        statcode, resp = agent.read_datafeed(id)
        print('read datafeed status code: ')
        print(statcode)
        print('read datafeed response')
        print(resp)
        #parsed_json = json.loads(resp)
        if len(resp) > 0 :
            echomsg = resp[0].get('message')
            Userid = resp[0].get('fromUserId')

            print(echomsg)
            echomsgsplit1 = echomsg.split('<messageML>')
            if echomsgsplit1[1].startswith('<mention uid="USER_ID"/>'):
                msg_actual = echomsgsplit1[1].lstrip('<mention uid="USER_ID"/> ')
                msg_actual = msg_actual.rstrip('</messageML>')
                print(msg_actual)
                r = requests.post(ifttt_webhook, data={"value1":msg_actual})

                msgFormat = 'MESSAGEML'

                message = '<messageML>Nobody summons Megatron!</messageML>'
                # send message
                try:
                    status_code, retstring = agent.send_message(symphony_sid, msgFormat, message)
                    print "%s: %s" % (status_code, retstring)
                except:
                    print(retstring)


if __name__ == "__main__":
    main()
