class TestRoutes(object):

  def test_simple(self):
    pass
    #
    # with EipiphanyTestContext(EipiphanyContext()) as eip_context:
    #   source = TimeIntervalSource(1)
    #   processor = MyTestProcessor()
    #   eip_context.add_route_builder(MyRouteBuilder(source, processor))
    #   eip_context.mock_endpoint_and_skip('timer', processor, expected_message_count=2)
    #   eip_context.start()
    #
    #   assert len(eip_context.mock_endpoints[processor].exchanges) == 2
    #   assert str(eip_context.mock_endpoints[processor].exchanges[0].body).startswith(str(datetime.now())[0:10])
    #   assert str(eip_context.mock_endpoints[processor].exchanges[1].body).startswith(str(datetime.now())[0:10])

