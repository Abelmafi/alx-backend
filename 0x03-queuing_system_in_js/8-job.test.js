const kue = require('kue');
const createPushNotificationsJobs = require('./8-job');

describe('createPushNotificationsJobs', () => {
  let queue;

  before(() => {
    queue = kue.createQueue();
    queue.testMode.enter();
  });

  after(() => {
    queue.testMode.clear();
    queue.testMode.exit();
  });

  it('should create jobs and add them to the queue', (done) => {
    const jobs = [
      {
        phoneNumber: '4153518780',
        message: 'This is the code 1234 to verify your account'
      },
      {
        phoneNumber: '4153518781',
        message: 'This is the code 4562 to verify your account'
      },
      {
        phoneNumber: '4153518743',
        message: 'This is the code 4321 to verify your account'
      }
    ];

    createPushNotificationsJobs(jobs, queue);

    setTimeout(() => {
      const createdJobs = queue.testMode.jobs;

      // Assert the number of created jobs
      expect(createdJobs.length).to.equal(jobs.length);

      // Add more assertions if needed

      done();
    }, 500);
  });
});

