def test_simple_fs_task(self):
    result = self.agent_system.assign_task("read a file") #Very simple task.
    self.assertIsNotNone(result[0]) #check that an agent is assigned.
    self.assertEqual(result[0].name, "FS Agent") #Check that the correct agent is selected.