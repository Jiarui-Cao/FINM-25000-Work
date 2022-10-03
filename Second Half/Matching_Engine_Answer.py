'''
References:
Sorting for price then time: https://www.kite.com/python/answers/how-to-sort-by-two-keys-in-python
Removing elements while iterating: https://stackoverflow.com/questions/1207406/how-to-remove-items-from-a-list-while-iterating

'''
class MatchingEngine():
    def __init__(self):
        self.bid_book = []
        self.ask_book = []
        # These are the order books you are given and expected to use for matching the orders below

    # Note: As you implement the following functions keep in mind that these enums are available:
#     class OrderType(Enum):
#         LIMIT = 1
#         MARKET = 2
#         IOC = 3

#     class OrderSide(Enum):
#         BUY = 1
#         SELL = 2
    '''
    Handle filled orders by breaking up order into bid-ask pairs
    [(bid 5, 12), (ask, 5,12),(bid,5,11),(ask,5,11))]


    '''
    def handle_order(self, order):
        # Implement this function
        # In this function you need to call different functions from the matching engine
        # depending on the type of order you are given
        results = None
        if type(order) == LimitOrder:
            results = self.handle_limit_order(order)
        elif type(order) == MarketOrder:
            results = self.handle_market_order(order)
        elif type(order) == IOCOrder:
            results = self.handle_ioc_order(order)
        # You need to raise the following error if the type of order is ambiguous
        else:
            raise UndefinedOrderType("Undefined Order Type!")
        return results

    def handle_limit_order(self, order):
        # Implement this function
        # Keep in mind what happens to the orders in the limit order books when orders get filled
        # or if there are no crosses from this order
        # in other words, handle_limit_order accepts an arbitrary limit order that can either be
        # filled if the limit order price crosses the book, or placed in the book. If the latter,
        # pass the order to insert_limit_order below.
        if order.side not in [OrderSide.BUY, OrderSide.SELL]:
            raise UndefinedOrderSide("Undefined Order Side!")
        filled_orders = []
        remove_list = []
        original_quantity=order.quantity
        order_quantity_filled = 0
        cost = 0
        # The orders that are filled from the market order need to be inserted into the above list
        if order.side == OrderSide.BUY:
            # for buy order, have to check all the sell orders
            # loop over ask spread starting from lowest price and going up until it reaches max price then break
            # decrement order.quantity, then pass in order into insert
            for ask_order in self.ask_book[:]:
                if ask_order.price <= order.price:
                    pass
                    # check relative quantities
                    # if order.quantity > ask_order.quantity:
                    # completely fill the ask order, appending it to filled order
                    # decrease order.quantity by that amount
                    # continue on to next order
                    if order.quantity > ask_order.quantity:
                        # do you have to decrement ask_order?
                        '''
                                                REDO WITH MAKING FILLED ORDERED

                                                '''
                        order.quantity -= ask_order.quantity

 


                        # filled_orders.append(ask_order)
                        order_quantity_filled += ask_order.quantity
                        temp_time = time.time()

                        #bid
                        filled_orders.append(FilledOrder(id=order.id,symbol=order.symbol,
                                                         quantity=ask_order.quantity,price=ask_order.price,
                                                         side=order.side,time=temp_time))
                        # ask
                        filled_orders.append(FilledOrder(id=ask_order.id,symbol=ask_order.symbol,
                                                         quantity=ask_order.quantity,price=ask_order.price,
                                                         side=ask_order.side,time=temp_time))
                        cost += ask_order.quantity * ask_order.price
                        # if changing iterator error, just append to filled orders then pop all of them at end
                        self.ask_book.remove(ask_order)

                    # if order.quantity < ask_order.quantity:
                    # decrease ask_order.quantity by order.quantity
                    elif order.quantity < ask_order.quantity:
                        # do you have to decrement ask_order?
                        ask_order.quantity -= order.quantity
                        # filled_orders.append(order)
                        order_quantity_filled += order.quantity
                        cost += order.quantity * ask_order.price
                        temp_time = time.time()
                        # bid
                        filled_orders.append(FilledOrder(order.id,symbol=order.symbol,quantity=order.quantity,
                                                         price=ask_order.price,side=order.side,
                                                         time=temp_time)) # Volume weighted average?
                        # filled_orders.append(ask_order)
                        # ask
                        filled_orders.append(FilledOrder(ask_order.id,ask_order.symbol,order.quantity,
                                                         price=ask_order.price,side=ask_order.side,time=temp_time))
                        break

                    # if order.quantity == ask_order.quantity:
                    # completely fill the ask order, appending it to filled order,
                    # break out of loop
                    # can maybe check in above case
                    elif order.quantity == ask_order.quantity:
                        cost += order.quantity * ask_order.price
                        order_quantity_filled += order.quantity
                        # filled_orders.append(order)
                        temp_time = time.time()
                        # bid
                        filled_orders.append(FilledOrder(order.id, symbol=order.symbol, quantity=order.quantity,
                                                         price=ask_order.price, side=order.side,
                                                         time=temp_time))  # Volume weighted average?
                        # filled_orders.append(ask_order)
                        # ask
                        filled_orders.append(FilledOrder(ask_order.id,ask_order.symbol,order.quantity,price=ask_order.price,
                                                         side=ask_order.side,time=temp_time))

                        self.ask_book.remove(ask_order)

                else:
                    break
            if order.quantity > 0:
                # if order_quantity_filled != 0:
                    # filled_orders.append(FilledOrder(order.id,symbol=order.symbol,
                    #                                  quantity=order_quantity_filled, price= (cost/order_quantity_filled),
                    #                                  time=order.time,side=order.side))
                self.insert_limit_order(order)

        if order.side == OrderSide.SELL:
            # for sell order, have to check all the buy orders
            # loop over ask spread starting from highest price and going up until it reaches min price then break
            # decrement order.quantity, then pass in order into insert

            for bid_order in self.bid_book[:]:
                if bid_order.price >= order.price:

                    # check relative quantities
                    # if order.quantity > ask_order.quantity:
                    # completely fill the ask order, appending it to filled order
                    # decrease order.quantity by that amount
                    # continue on to next order
                    if order.quantity > bid_order.quantity:
                        # do you have to decrement ask_order?
                        # print(f'order quantity was {order.quantity}')

                        order.quantity -= bid_order.quantity
                        order_quantity_filled += bid_order.quantity
                        cost += order.quantity * bid_order.price
                        # print(f'order quantity is now {order.quantity}')
                        # filled_orders.append(bid_order)
                        temp_time = time.time()
                        # bid order
                        filled_orders.append(FilledOrder(id=bid_order.id,symbol=bid_order.symbol,
                                                         quantity=bid_order.quantity,price=bid_order.price,
                                                         side=bid_order.side,time=temp_time))
                        # ask order
                        filled_orders.append(FilledOrder(id=order.id,symbol=order.symbol,
                                                         quantity=bid_order.quantity,price=bid_order.price,
                                                         side=order.side,time=temp_time))

                        # ask order
                        # if changing iterator error, just append to filled orders then pop all of them at end
                        self.bid_book.remove(bid_order)


                    # if order.quantity < ask_order.quantity:
                    # decrease ask_order.quantity by order.quantity
                    elif order.quantity < bid_order.quantity:
                        # do you have to decrement ask_order?
                        # print(f'bid order quantity was {bid_order.quantity}')
                        bid_order.quantity -= order.quantity
                        # print(f'bid order quantity is now {bid_order.quantity}')
                        # filled_orders.append(order)
                        order_quantity_filled += order.quantity
                        cost += order.quantity * bid_order.price
                        temp_time = time.time()
                        # bid
                        filled_orders.append(FilledOrder(id=bid_order.id,symbol=bid_order.symbol,quantity=order.quantity,
                                                         price=bid_order.price,side=bid_order.side,time=temp_time))
                        # ask
                        filled_orders.append(FilledOrder(order.id,symbol=order.symbol,quantity=order.quantity,
                                                         price=bid_order.price,side=order.side,
                                                         time=temp_time)) # Volume weighted average?

                        # filled_orders.append(bid_order)
                        # fill ask


                        # can also consider appending another instance with same attributes
                        break

 


                    # if order.quantity == ask_order.quantity:
                    # completely fill the ask order, appending it to filled order,
                    # break out of loop
                    # can maybe check in above case
                    elif order.quantity == bid_order.quantity:
                        cost += order.quantity * bid_order.price
                        order_quantity_filled += order.quantity
                        # filled_orders.append(order)
                        temp_time = time.time()
                        # bid
                        filled_orders.append(FilledOrder(id=bid_order.id,symbol=bid_order.symbol,quantity=order.quantity,
                                                         price=bid_order.price,side=bid_order.side,time=temp_time))
                        # ask
                        filled_orders.append(FilledOrder(order.id,symbol=order.symbol,quantity=order.quantity,
                                                         price=bid_order.price,side=order.side,
                                                         time=temp_time)) # Volume weighted average?

                        self.bid_book.remove(bid_order)

                else:
                    break
            if order.quantity > 0:
                # if order.quantity > 0:
                #     if order_quantity_filled != 0:
                #         filled_orders.append(FilledOrder(order.id, symbol=order.symbol,
                #                                          quantity=order_quantity_filled,
                #                                          price=(cost / order_quantity_filled),
                #                                          time=order.time, side=order.side))
                self.insert_limit_order(order)
        # The filled orders are expected to be the return variable (list)
        # for filled_order in filled_orders:


        return filled_orders

        # You need to raise the following error if the side the order is for is ambiguous
        # raise UndefinedOrderSide("Undefined Order Side!")


    def handle_market_order(self, order):
        # Implement this function
        if order.side not in [OrderSide.BUY, OrderSide.SELL]:
            raise UndefinedOrderSide("Undefined Order Side!")

        filled_orders = []
        original_quantity=order.quantity
        order_quantity_filled = 0
        cost = 0
        # The orders that are filled from the market order need to be inserted into the above list

        # copy of limit order. Need to Adjust!
        if order.side == OrderSide.BUY:
            for ask_order in self.ask_book[:]:
                if order.quantity > ask_order.quantity:
                    # do you have to decrement ask_order?
                    order.quantity -= ask_order.quantity
                    # filled_orders.append(ask_order)
                    order_quantity_filled += ask_order.quantity
                    temp_time = time.time()
                    #bid
                    filled_orders.append(
                        FilledOrder(id=order.id, symbol=order.symbol, quantity=ask_order.quantity,
                                    price=ask_order.price, side=order.side, time=temp_time))
                    # ask
                    filled_orders.append(
                        FilledOrder(id=ask_order.id, symbol=ask_order.symbol, quantity=ask_order.quantity,
                                    price=ask_order.price, side=ask_order.side, time=temp_time))

                    cost += ask_order.quantity * ask_order.price
                    # if changing iterator error, just append to filled orders then pop all of them at end
                    self.ask_book.remove(ask_order)
                elif order.quantity < ask_order.quantity:
                    # do you have to decrement ask_order?
                    ask_order.quantity -= order.quantity
                    # filled_orders.append(order)
                    # filled_orders.append(ask_order)
                    order_quantity_filled += order.quantity
                    cost += order.quantity * ask_order.price
                    temp_time = time.time()
                    # bid
                    filled_orders.append(FilledOrder(order.id, symbol=order.symbol, quantity=order.quantity,
                                                     price=ask_order.price, side=order.side,
                                                     time=temp_time))  # Volume weighted average?
                    # filled_orders.append(ask_order)
                    # ask
                    filled_orders.append(
                        FilledOrder(ask_order.id, ask_order.symbol, order.quantity, price=ask_order.price,
                                    side=ask_order.side, time=temp_time))

                    break

                # if order.quantity == ask_order.quantity:
                # completely fill the ask order, appending it to filled order,
                # break out of loop
                # can maybe check in above case
                elif order.quantity == ask_order.quantity:
                    # filled_orders.append(order)
                    # filled_orders.append(ask_order)
                    cost += order.quantity * ask_order.price
                    order_quantity_filled += order.quantity
                    # filled_orders.append(order)
                    temp_time = time.time()
                    #bid
                    filled_orders.append(FilledOrder(order.id, symbol=order.symbol, quantity=order.quantity,
                                                     price=ask_order.price, side=order.side,
                                                     time=temp_time))  # Volume weighted average?
                    # filled_orders.append(ask_order)
                    # ask
                    filled_orders.append(
                        FilledOrder(ask_order.id, ask_order.symbol, order.quantity, price=ask_order.price,
                                    side=ask_order.side, time=temp_time))

                    self.ask_book.remove(ask_order)
                # if ask_order.price <= order.price:
                #     pass
                #     # check relative quantities
                #     # if order.quantity > ask_order.quantity:
                #     # completely fill the ask order, appending it to filled order
                #     # decrease order.quantity by that amount
                #     # continue on to next order
                #     if order.quantity > ask_order.quantity:
                #         # do you have to decrement ask_order?
                #         order.quantity -= ask_order.quantity
                #         filled_orders.append(ask_order)
                #         # if changing iterator error, just append to filled orders then pop all of them at end
                #         self.ask_book.remove(ask_order)
                #
                #     # if order.quantity < ask_order.quantity:
                #     # decrease ask_order.quantity by order.quantity
                #     if order.quantity < ask_order.quantity:
                #         # do you have to decrement ask_order?
                #         order.quantity -= ask_order.quantity
                #         filled_orders.append(order)
                #         filled_orders.append(ask_order)
                #         break

                    # if order.quantity == ask_order.quantity:
                    # completely fill the ask order, appending it to filled order,
                    # break out of loop
                    # can maybe check in above case
                    # if order.quantity == ask_order.quantity:
                    #     filled_orders.append(order)
                    #     filled_orders.append(ask_order)
                    #     self.ask_book.remove(ask_order)

                else:
                    break
            # if order.quantity > 0:
            #     self.insert_limit_order(order)
        if order.side == OrderSide.SELL:
            # for sell order, have to check all the buy orders
            # loop over ask spread starting from highest price and going up until it reaches min price then break
            # decrement order.quantity, then pass in order into insert

            for bid_order in self.bid_book[:]:
                if order.quantity > bid_order.quantity:
                    # do you have to decrement ask_order?
                    # print(f'order quantity was {order.quantity}')
                    order.quantity -= bid_order.quantity
                    # print(f'order quantity is now {order.quantity}')
                    # filled_orders.append(bid_order)
                    # order.quantity -= bid_order.quantity
                    order_quantity_filled += bid_order.quantity
                    cost += order.quantity * bid_order.price
                    # print(f'order quantity is now {order.quantity}')
                    # filled_orders.append(bid_order)
                    temp_time = time.time()
                    # bid
                    filled_orders.append(
                        FilledOrder(id=bid_order.id, symbol=bid_order.symbol, quantity=bid_order.quantity,
                                    price=bid_order.price, side=bid_order.side, time=temp_time))
                    # ask
                    filled_orders.append(
                        FilledOrder(id=order.id, symbol=order.symbol, quantity=bid_order.quantity,
                                    price=bid_order.price, side=order.side, time=temp_time))
                    # if changing iterator error, just append to filled orders then pop all of them at end
                    self.bid_book.remove(bid_order)


                # if order.quantity < ask_order.quantity:
                # decrease ask_order.quantity by order.quantity
                elif order.quantity < bid_order.quantity:
                    # do you have to decrement ask_order?
                    # print(f'bid order quantity was {bid_order.quantity}')
                    bid_order.quantity -= order.quantity
                    # print(f'bid order quantity is now {bid_order.quantity}')

                    # filled_orders.append(bid_order)
                    # filled_orders.append(order)
                    order_quantity_filled += order.quantity
                    cost += order.quantity * bid_order.price
                    temp_time = time.time()
                    # bid
                    filled_orders.append(FilledOrder(id=bid_order.id, symbol=bid_order.symbol, quantity=order.quantity,
                                                     price=bid_order.price, side=bid_order.side, time=temp_time))

                    # ask
                    filled_orders.append(FilledOrder(order.id, symbol=order.symbol, quantity=order.quantity,
                                                     price=bid_order.price, side=order.side,
                                                     time=temp_time))  # Volume weighted average?
                    # filled_orders.append(bid_order)


                    break

 


                # if order.quantity == ask_order.quantity:
                # completely fill the ask order, appending it to filled order,
                # break out of loop
                # can maybe check in above case
                elif order.quantity == bid_order.quantity:
                    # filled_orders.append(bid_order)
                    # filled_orders.append(order)
                    cost += order.quantity * bid_order.price
                    order_quantity_filled += order.quantity
                    # filled_orders.append(order)
                    temp_time = time.time()
                    # bid
                    filled_orders.append(
                        FilledOrder(bid_order.id, bid_order.symbol, order.quantity, price=bid_order.price,
                                    side=bid_order.side, time=temp_time))
                    # ask
                    filled_orders.append(FilledOrder(order.id, symbol=order.symbol, quantity=order.quantity,
                                                     price=bid_order.price, side=order.side,
                                                     time=temp_time))  # Volume weighted average?
                    # filled_orders.append(ask_order)
                    # ask

                    self.bid_book.remove(bid_order)

                else:
                    break
        # The filled orders are expected to be the return variable (list)
        return filled_orders

        # You need to raise the following error if the side the order is for is ambiguous
        # raise UndefinedOrderSide("Undefined Order Side!")


    def handle_ioc_order(self, order):
        # Implement this function
        if order.side not in [OrderSide.BUY, OrderSide.SELL]:
            raise UndefinedOrderSide("Undefined Order Side!")
        filled_orders = []
        remove_list = []
        temp_quantity = order.quantity
        original_quantity=order.quantity
        order_quantity_filled = 0
        cost = 0
        # The orders that are filled from the ioc order need to be inserted into the above list

        # segment copied from limit order function
        # instead of removing during loop, put orders to be remove in remove_list
        # can commit changes if reaching order.quantity < ask/bid_order.quantity or order.quantity == ask/bide_order.quantity


        if order.side == OrderSide.BUY:
            # for buy order, have to check all the sell orders
            # loop over ask spread starting from lowest price and going up until it reaches max price then break
            # decrement order.quantity, then pass in order into insert
            for ask_order in self.ask_book[:]:
                if ask_order.price <= order.price:
                    pass
                    # check relative quantities
                    # if order.quantity > ask_order.quantity:
                    # completely fill the ask order, appending it to filled order
                    # decrease order.quantity by that amount
                    # continue on to next order
                    if temp_quantity > ask_order.quantity:
                        # do you have to decrement ask_order?
                        temp_quantity -= ask_order.quantity
                        cost += ask_order.quantity * ask_order.price
                        # filled_orders.append(ask_order)
                        # if changing iterator error, just append to filled orders then pop all of them at end
                        remove_list.append(ask_order)
                        # self.ask_book.remove(ask_order)

                    # if order.quantity < ask_order.quantity:
                    # decrease ask_order.quantity by order.quantity
                    elif temp_quantity < ask_order.quantity:
                        # do you have to decrement ask_order?
                        ask_order.quantity -= temp_quantity
                        cost += ask_order.quantity * ask_order.price
                        for order_to_remove in remove_list:
                            # filled_orders.append(ask_order)
                            temp_time =time.time()
                            # bid order
                            filled_orders.append(
                                FilledOrder(order.id, order.symbol, order_to_remove.quantity,
                                            price=order_to_remove.price,
                                            side=order.side, time=temp_time))
                            # ask
                            filled_orders.append(
                                FilledOrder(order_to_remove.id, order_to_remove.symbol, order_to_remove.quantity, price=order_to_remove.price,
                                            side=order_to_remove.side, time=temp_time))
                            # ask order

                            self.ask_book.remove(order_to_remove)
                        # filled_orders.append(order)
                        temp_time = time.time()
                        # bid
                        filled_orders.append(FilledOrder(order.id, symbol=order.symbol, quantity=temp_quantity,
                                                         price=ask_order.price, side=order.side,
                                                         time=temp_time))  # Volume weighted average?
                        # filled_orders.append(ask_order)
                        #ask
                        filled_orders.append(
                            FilledOrder(ask_order.id, ask_order.symbol, temp_quantity, price=ask_order.price,
                                        side=ask_order.side, time=temp_time))

                        return filled_orders

                    # if order.quantity == ask_order.quantity:
                    # completely fill the ask order, appending it to filled order,
                    # break out of loop
                    # can maybe check in above case
                    elif temp_quantity == ask_order.quantity:
                        cost += ask_order.quantity * ask_order.price
                        for order_to_remove in remove_list:
                            # filled_orders.append(ask_order)
                            temp_time =time.time()
                            # bid order
                            filled_orders.append(
                                FilledOrder(order.id, order.symbol, order_to_remove.quantity,
                                            price=order_to_remove.price,
                                            side=order.side, time=temp_time))
                            # ask
                            filled_orders.append(
                                FilledOrder(order_to_remove.id, order_to_remove.symbol, order_to_remove.quantity, price=order_to_remove.price,
                                            side=order_to_remove.side, time=temp_time))
                            # ask order

                            self.ask_book.remove(order_to_remove)
                        # filled_orders.append(order)
                        temp_time = time.time()
                        #bid
                        filled_orders.append(FilledOrder(order.id, symbol=order.symbol, quantity=temp_quantity,
                                                         price=ask_order.price, side=order.side,
                                                         time=temp_time))  # Volume weighted average?
                        # filled_orders.append(ask_order)
                        #ask
                        filled_orders.append(
                            FilledOrder(ask_order.id, ask_order.symbol, temp_quantity, price=ask_order.price,
                                        side=ask_order.side, time=temp_time))
                        return filled_orders
                else:
                    break
            if temp_quantity > 0:
                # self.insert_limit_order(order)
                # print('Could not fill IOC buy order')
                del remove_list
                return None

 

        if order.side == OrderSide.SELL:
            # for sell order, have to check all the buy orders
            # loop over ask spread starting from highest price and going up until it reaches min price then break
            # decrement order.quantity, then pass in order into insert

            for bid_order in self.bid_book[:]:
                if bid_order.price >= order.price:

                    # check relative quantities
                    # if order.quantity > ask_order.quantity:
                    # completely fill the ask order, appending it to filled order
                    # decrease order.quantity by that amount
                    # continue on to next order
                    if temp_quantity > bid_order.quantity:
                        # do you have to decrement ask_order?
                        temp_quantity -= bid_order.quantity
                        cost += bid_order.quantity * bid_order.price
                        # filled_orders.append(ask_order)
                        # if changing iterator error, just append to filled orders then pop all of them at end
                        remove_list.append(bid_order)
                        # self.ask_book.remove(ask_order)


                    # if order.quantity < ask_order.quantity:
                    # decrease ask_order.quantity by order.quantity
                    elif temp_quantity < bid_order.quantity:
                        # do you have to decrement ask_order?
                        cost += bid_order.quantity * bid_order.price
                        bid_order.quantity -= temp_quantity

                        for order_to_remove in remove_list:
                            # filled_orders.append(bid_order)
                            temp_time = time.time()
                            # bid
                            filled_orders.append(
                                FilledOrder(order_to_remove.id, order_to_remove.symbol, order_to_remove.quantity, price=order_to_remove.price,
                                            side=order_to_remove.side, time=temp_time))
                            # ask
                            filled_orders.append(
                                FilledOrder(order_to_remove.id, order_to_remove.symbol, order_to_remove.quantity, price=order_to_remove.price,
                                            side=order_to_remove.side, time=temp_time))
                            self.bid_book.remove(order_to_remove)
                        # filled_orders.append(order)
                        temp_time = time.time()
                        # bid
                        filled_orders.append(
                            FilledOrder(bid_order.id, bid_order.symbol, temp_quantity, price=bid_order.price,
                                        side=bid_order.side, time=temp_time))
                        #  ask
                        filled_orders.append(FilledOrder(order.id, symbol=order.symbol, quantity=temp_quantity,
                                                         price=bid_order.price, side=order.side,
                                                         time=temp_time))  # Volume weighted average?
                        # filled_orders.append(bid_order)
                        # ask

                        return filled_orders

 

                    # if order.quantity == ask_order.quantity:
                    # completely fill the ask order, appending it to filled order,
                    # break out of loop
                    # can maybe check in above case
                    elif temp_quantity == bid_order.quantity:
                        cost += bid_order.quantity * bid_order.price
                        for order_to_remove in remove_list:
                            # filled_orders.append(bid_order)
                            temp_time = time.time()
                            # bid
                            filled_orders.append(
                                FilledOrder(order_to_remove.id, bid_order.symbol, order_to_remove.quantity, price=order_to_remove.price,
                                            side=order_to_remove.side, time=temp_time))
                            # ask
                            filled_orders.append(
                                FilledOrder(order.id, order.symbol, order_to_remove.quantity, price=order_to_remove.price,
                                            side=order.side, time=temp_time))
                            self.bid_book.remove(order_to_remove)
                        # filled_orders.append(order)
                        temp_time = time.time()
                        # bid
                        filled_orders.append(
                            FilledOrder(bid_order.id, bid_order.symbol, temp_quantity, price=bid_order.price,
                                        side=bid_order.side, time=temp_time))
                        # ask
                        filled_orders.append(FilledOrder(order.id, symbol=order.symbol, quantity=temp_quantity,
                                                         price=bid_order.price, side=order.side,
                                                         time=temp_time))  # Volume weighted average?
                        # filled_orders.append(bid_order)

                        return filled_orders

                else:
                    break
            if temp_quantity > 0:
                # self.insert_limit_order(order)
                # print('Could not fill IOC buy order')
                del remove_list
                return filled_orders
        # The filled orders are expected to be the return variable (list)
        return filled_orders

        # You need to raise the following error if the side the order is for is ambiguous
        # raise UndefinedOrderSide("Undefined Order Side!")


    def insert_limit_order(self, order):
        assert order.type == OrderType.LIMIT
        # Implement this function
        # this function's sole puporse is to place limit orders in the book that are guaranteed
        # to not immediately fill
        if order.side == OrderSide.BUY:
            self.bid_book.append(order)
            # want both price and time to be in ascending
            self.bid_book.sort(key=lambda x: (-1* x.price,x.time),reverse=False)
            # print(f'sorted bid book: {self.bid_book} after inserting {order}')

        elif order.side == OrderSide.SELL:
            self.ask_book.append(order)
            # want highest price last, but earliest time first
            # can either sort twice or use negative
            self.ask_book.sort(key=lambda x: (1 * x.price,x.time),reverse=False)
            # print(f'sorted ask book: {self.ask_book} after inserting {order}')
        # You need to raise the following error if the side the order is for is ambiguous
        else:
            raise UndefinedOrderSide("Undefined Order Side!")

    def amend_quantity(self, id, quantity):
        # Implement this function
        # Hint: Remember that there are two order books, one on the bid side and one on the ask side
        for order in self.bid_book:
            if order.id == id:
                if quantity <= order.quantity:
                    order.quantity = quantity
                    # print('order found in bid book, reducing quantity')
                    return True
                else:
                    raise NewQuantityNotSmaller("Amendment Must Reduce Quantity!")
        for order in self.ask_book:
            if order.id == id:
                if quantity <= order.quantity:
                    order.quantity = quantity
                    # print('order found in bid book, reducing quantity')
                    return True
                else:
                    raise NewQuantityNotSmaller("Amendment Must Reduce Quantity!")
        # You need to raise the following error if the user attempts to modify an order
        # with a quantity that's greater than given in the existing order

        # raise NewQuantityNotSmaller("Amendment Must Reduce Quantity!")
        return False

    def cancel_order(self, id):
        # Implement this function
        # Think about the changes you need to make in the order book based on the parameters given
        for order in self.bid_book:
            if order.id == id:
                del order
                return True
        for order in self.ask_book:
            if order.id == id:
                del order
                return True
        return False
